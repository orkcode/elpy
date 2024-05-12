from datetime import datetime
from promelec.models import PromelecCategory
import re


def convert_date_to_django_format(date_str):
    date_part = date_str.split(': ')[1]
    date_obj = datetime.strptime(date_part, '%d.%m.%Y %H:%M')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
    return formatted_date


async def create_categories(path):
    parent = None
    for category_name in path:
        category = await PromelecCategory.objects.filter(name=category_name, parent=parent).afirst()
        if not category:
            category = await PromelecCategory.objects.acreate(name=category_name, parent=parent)
        parent = category
    return parent


async def compare_warehouse(current_data, previous_data):
    changes = {
        'price_changes': [],
        'reserves': []
    }

    current_warehouses = {wh['name']: wh for wh in current_data['warehouses']}
    previous_warehouses = {wh['name']: wh for wh in previous_data['warehouses']}

    for name, current_wh in current_warehouses.items():
        previous_wh = previous_warehouses.get(name)
        if previous_wh:
            current_prices = current_wh.get('prices', {})
            previous_prices = previous_wh.get('prices', {})
            for quantity, price in current_prices.items():
                if quantity in previous_prices and price != previous_prices[quantity]:
                    changes['price_changes'].append({
                        'warehouse': name,
                        'quantity': quantity,
                        'old_price': previous_prices[quantity],
                        'new_price': price
                    })
            current_qty = current_wh['availability']['quantity']
            previous_qty = previous_wh['availability']['quantity']
            if current_qty != previous_qty:
                change_type = 'пополнение' if current_qty > previous_qty else 'продажа'
                changes['reserves'].append({
                    'warehouse': name,
                    'price': current_wh['prices'][quantity],
                    'change_type': change_type,
                    'quantity_change': abs(current_qty - previous_qty)
                })
    return changes
