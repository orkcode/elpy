import random
from django.core.management.base import BaseCommand
from promelec.models import SitemapURL
from promelec.tasks import run_spider

# List of proxy IPs
PROXY_LIST = [
    'http://proxy1:port',
    'http://proxy2:port',
    # Add more proxies as needed
]

class Command(BaseCommand):
    help = 'Enqueues Scrapy spiders for each SitemapURL with unique proxies'

    def handle(self, *args, **options):
        sitemap_urls = SitemapURL.objects.all()
        for sitemap_url in sitemap_urls:
            proxy = random.choice(PROXY_LIST)
            run_spider.delay(sitemap_url.url, proxy)