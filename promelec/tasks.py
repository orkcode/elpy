from billiard.context import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import csv
import asyncio
from celery import shared_task
from asgiref.sync import sync_to_async
from django.conf import settings
from scraper.spiders.promelec_sitemap import SitemapSpider
from promelec.models import PromelecInventory, PromelecProduct, PromelecOrder
from promelec.utils import compare_warehouse, create_categories, convert_date_to_django_format, split_urls
from celery.utils.log import get_task_logger
from core.transaction import AsyncAtomic
from scraper.spiders.promelec_sitemap import PromElecSitemapSpider
from promelec.models import PromelecBrand, PromelecInventory, PromelecProduct, PromelecOrder, StateOder, SitemapURL
from itemadapter import ItemAdapter
import subprocess

logger = get_task_logger(__name__)


@sync_to_async
def get_inventories():
    return PromelecInventory.objects.select_related('product__brand', 'product__category').all()


async def generate_csv_file():
    path = f'{settings.MEDIA_ROOT}/prom/inventory.csv'
    header = ['Товар', 'Категория', 'Бренд', 'Дата обновления', 'Склады']

    try:
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            async for inventory in await get_inventories():
                product = inventory.product
                writer.writerow([
                    product.part_number, product.category.name, product.brand.name,
                    inventory.updated_date.strftime('%Y-%m-%d %H:%M:%S'),
                    inventory.data.get('warehouses', '')
                ])
    except Exception as e:
        logger.error(f"Error generating CSV: {e}")


@shared_task
def generate_inventory_csv():
    asyncio.run(generate_csv_file())


async def item_task(part_number, manufacturer, product_code, breadcrumbs, warehouses, updated_at):
    async with AsyncAtomic():
        brand, created = await PromelecBrand.objects.aget_or_create(name=manufacturer)
        product, created = await PromelecProduct.objects.aget_or_create(
            category=await create_categories(breadcrumbs),
            part_number=part_number,
            brand=brand,
            product_code=product_code
        )
        updated_date = convert_date_to_django_format(updated_at)
        inventory_exists = await PromelecInventory.objects.filter(product=product, updated_date=updated_date).aexists()
        if inventory_exists:
            return

        await PromelecInventory.objects.aget_or_create(
            product=product,
            updated_date=updated_date,
            defaults={'data': {'warehouses': warehouses}}
        )
        current_warehouse = {'warehouses': warehouses}
        previous_inventory = await PromelecInventory.objects.filter(product=product).order_by('-updated_date')[
                                   1:2].afirst()
        if previous_inventory:
            changes = await compare_warehouse(current_warehouse, previous_inventory.data)
            reserves = changes.get('reserves', [])
            objects_2_create = []
            for reserve in reserves:
                state = StateOder.RESTOCK_VERIFICATION if reserve[
                                                              'change_type'] == 'RESTOCK' else StateOder.SOLD_VERIFICATION
                objects_2_create.append(PromelecOrder(
                    product=product,
                    quantity=reserve['quantity_change'],
                    warehouse=reserve['warehouse'],
                    price=reserve['price'],
                    state=state
                ))
            await PromelecOrder.objects.abulk_create(objects_2_create)


@shared_task
def process_item_task(*args, **kwargs):
    asyncio.run(item_task(*args, **kwargs))


class WebScraperRunner:
    def __init__(self, settings=None):
        if settings is None:
            settings = get_project_settings()
        self.crawler = CrawlerProcess(settings)

    def _crawl(self):
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, spider_cls, *args, **kwargs):
        self.crawler.crawl(spider_cls, *args, **kwargs)

    def run(self):
        p = Process(target=self._crawl)
        p.start()
        p.join()

@shared_task()
def fetch_goods_xml_urls():
    crawler = WebScraperRunner()
    crawler.crawl(PromElecSitemapSpider)
    crawler.run()
