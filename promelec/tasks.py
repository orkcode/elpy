from celery import shared_task
import csv
import asyncio
from celery import shared_task
from asgiref.sync import sync_to_async
from django.conf import settings
from promelec.models import PromelecInventory, PromelecProduct, PromelecOrder
from promelec.utils import compare_warehouse
from celery.utils.log import get_task_logger

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


async def get_inventory(product, index):
    inventory_list = await sync_to_async(list)(
        PromelecInventory.objects.filter(product=product).order_by('-updated_date').values('data')[index:index+1]
    )
    return inventory_list[0] if inventory_list else None


async def analyze_scraped_items():
    async for product in PromelecProduct.objects.all():
        current_inventory = await get_inventory(product, 0)
        previous_inventory = await get_inventory(product, 1)
        if not current_inventory or not previous_inventory:
            continue

        changes = await compare_warehouse(current_inventory['data'], previous_inventory['data'])
        reserves = changes.get('reserves', [])
        objects_2_create = []
        for reserve in reserves:
            objects_2_create.append(PromelecOrder(
                product=await PromelecProduct.objects.filter(part_number=product.part_number).afirst(),
                quantity=reserve['quantity_change'],
                warehouse=reserve['warehouse'],
                price=reserve['price']
            ))
        await PromelecOrder.objects.abulk_create(objects_2_create, batch_size=100, ignore_conflicts=True)


@shared_task
def analyze_inventory_changes():
    asyncio.run(analyze_scraped_items())


#async def analyze_scraped_items():
#    async for product in PromelecProduct.objects.all():
#        print(f"Analyzin")
#
#@shared_task
#def analyze_inventory_changes():
#    asyncio.run(analyze_scraped_items())
