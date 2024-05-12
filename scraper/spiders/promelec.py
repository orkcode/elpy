import scrapy
from scrapy.spiders import SitemapSpider, Spider
from scraper.items import PromelecItem


class PromElecSpider(scrapy.Spider):
    name = 'promelec'
    allowed_domains = ["promelec.ru"]
    start_urls = ['https://www.promelec.ru/product/517355/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.PromelecDjangoPipeline': 300,
        }
    }

    def parse(self, response):
        item = PromelecItem()
        breadcrumbs = response.xpath(
            '//ul[@class="bread-crambs"]/li[@itemprop="itemListElement"]/a/span[@itemprop="name"]/text()').extract()
        item['breadcrumbs'] = breadcrumbs[2:]
        item['part_number'] = response.xpath(
            '//div[@class="popup-product-inf__right popup-product-inf__articul"]/text()').get()
        manufacturer = response.xpath('//a[@class="popup-product-inf__name"]/span/text()').get()
        item['manufacturer'] = manufacturer.strip() if manufacturer else 'Нет производителя'
        item['product_code'] = response.xpath('//div[contains(.,"Код товара:")]/span/text()').get().strip()
        item['updated_at'] = response.xpath('//div[@class="product-table__date"]/text()').get()
        table = response.xpath('//div[@class="popup-product-table"]')
        warehouses = table.xpath('.//div[@class="js-accordion-wrap"]')
        for warehouse in warehouses:
            name = warehouse.xpath('.//div[@class="popup-product-table__title hide-sm-mob"]/text()').get().strip()
            rows = warehouse.xpath('.//ul[@class="table-popup-list"]/li')
            for row in rows:
                prices = row.xpath(
                    './/div[@class="col-table col-table_2"]//span[@class="table-list__total-price price-color"]/text()').extract()
                prices = [float(price.replace(',', '.').replace(' ', '')) for price in prices]
                quantities = row.xpath(
                    './/div[@class="col-table col-table_1"]//span[@class="table-list__stocke"]/@data-min-qty').extract()
                quantities = [int(qty) for qty in quantities]
                lead_time_element = row.xpath(
                    './/div[@class="col-table col-table_3"]//span[@class="table-list__counter"]')
                lead_time_text = lead_time_element.xpath('string(.)').get().strip()
                price_dict = {quantity: price for quantity, price in zip(quantities, prices)}
                qty = row.xpath(
                    './/div[@class="col-table col-table_4"]//span[contains(@class, "table-list__counter")]/text()').get()
                qty = int(qty.replace(" ", "")) if qty else 0
                min_order = row.xpath(
                    './/div[@class="col-table col-table_7"]//span[@class="table-list__counter"]/text()').get()
                min_order = int(min_order.replace(" ", "")) if min_order else 0
                # Добавление данных о наличии на складе
                item.add_warehouse(
                    name=name,
                    prices=price_dict,
                    quantity=qty,
                    min_order=min_order,  # Предполагаем, что минимальный заказ совпадает с указанным количеством
                    lead_time=lead_time_text
                )

        yield item
