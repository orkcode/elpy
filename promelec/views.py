import os
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta
from adrf.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from promelec.tasks import generate_inventory_csv
from promelec.models import PromelecProduct, PromelecInventory, PromelecOrder
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from promelec.utils import compare_warehouse
import json


class GenerateOrDownloadCSVAPIView(APIView):
    async def get(self, request):
        csv_path = f'{settings.MEDIA_ROOT}/prom/inventory.csv'

        if os.path.exists(csv_path):
            return FileResponse(open(csv_path, 'rb'), as_attachment=True, filename='inventory.csv')
        else:
            generate_inventory_csv.delay()
            return HttpResponse("CSV файл генерируется.", status=202)


class GetBestOffer(APIView):
    async def get(self, request, part_number):
        product = await PromelecInventory.objects.filter(product__part_number=part_number).afirst()
        if product:
            min_price = float('inf')
            min_lead_time = None
            min_quantity = 0
            warehouse_name = None
            print(product.data)
            for warehouse in product.data['warehouses']:
                if warehouse['name'] == 'Оптовый склад «Промэлектроника»':
                    if warehouse['prices']:
                        min_price = min(warehouse['prices'].values())
                    min_lead_time = warehouse['availability']['lead_time']
                    min_quantity = warehouse['availability']['quantity']
                    warehouse_name = warehouse['name']
                    break
                else:
                    if warehouse['prices']:
                        for price in warehouse['prices'].values():
                            if price < min_price:
                                min_price = price
                                min_lead_time = warehouse['availability']['lead_time']
                                min_quantity = warehouse['availability']['quantity']
                                warehouse_name = warehouse['name']

            return JsonResponse({
                'part_number': part_number,
                'lowest_price': min_price,
                'total_quantity': min_quantity,
                'lead_time': min_lead_time,
                'updated_date': product.updated_date,
                'warehouses': warehouse_name
            })
        return JsonResponse({'error': 'Product not found'}, status=404)


class GetDayChanges(APIView):
    async def get(self, request):
        analyze_inventory_changes.delay()
        return JsonResponse({'message': 'Analyzing inventory changes. Please check back in a few moments.'}, status=202)

