import scrapy
from scrapy.item import Item, Field


class PromelecItem(Item):
    breadcrumbs = Field()
    part_number = Field()
    manufacturer = Field()
    product_code = Field()
    updated_at = Field()
    warehouses = Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['warehouses'] = []

    def add_warehouse(self, name, prices, quantity, min_order, lead_time=None):
        warehouse_data = {
            'name': name,
            'prices': prices,
            'availability': {
                'quantity': quantity,
                'min_order': min_order,
                'lead_time': lead_time
            }
        }
        self['warehouses'].append(warehouse_data)
