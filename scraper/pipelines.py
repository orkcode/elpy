# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from core.transaction import AsyncAtomic
from promelec.models import PromelecProduct, PromelecBrand, PromelecInventory, PromelecCategory
from promelec.utils import create_categories, convert_date_to_django_format


class PromelecDjangoPipeline:
    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        async with AsyncAtomic():
            brand, created = await PromelecBrand.objects.aget_or_create(name=adapter['manufacturer'])
            product, created = await PromelecProduct.objects.aget_or_create(
                category=await create_categories(adapter['breadcrumbs']),
                part_number=adapter['part_number'],
                brand=brand,
                product_code=adapter['product_code']
            )
            inventory = await PromelecInventory.objects.aget_or_create(
                product=product,
                updated_date=convert_date_to_django_format(adapter['updated_at']),
                defaults={'data': {'warehouses': adapter['warehouses']}}
            )
            return item