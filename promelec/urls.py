from django.urls import path
from promelec.views import GenerateOrDownloadCSVAPIView, GetBestOffer

urlpatterns = [
    path('csv/', GenerateOrDownloadCSVAPIView.as_view(), name='csv-api'),
    path('get_offer/<str:part_number>', GetBestOffer.as_view(), name='part-number-api'),
]