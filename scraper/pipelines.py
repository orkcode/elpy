# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from core.transaction import AsyncAtomic
from promelec.models import PromelecProduct, PromelecBrand, PromelecInventory, PromelecCategory, PromelecOrder, StateOder
from promelec.utils import create_categories, convert_date_to_django_format, compare_warehouse
from promelec.tasks import process_item_task


class PromelecDjangoPipeline:
    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        part_number = adapter.get('part_number')
        manufacturer = adapter.get('manufacturer')
        product_code = adapter.get('product_code')
        breadcrumbs = adapter.get('breadcrumbs')
        warehouses = adapter.get('warehouses')
        updated_at = adapter.get('updated_at')
        process_item_task.delay(part_number, manufacturer, product_code, breadcrumbs, warehouses, updated_at)
        return item