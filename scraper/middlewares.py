# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.python import to_bytes
from urllib.parse import urlparse, unquote
import base64
from scrapy import settings
from rotating_proxies.middlewares import RotatingProxyMiddleware
from rotating_proxies.expire import Proxies

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BrightProxyMiddleware(object):
    def __init__(self, settings):
        if not settings.getbool('BRIGHTDATA_ENABLED', True):
            raise NotConfigured

        self.proxy = settings.get('BRIGHTDATA_URL', 'http://127.0.0.1:24000')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy


class RProxyMiddleware:
    def __init__(self, proxy_list_path):
        self.proxy_list = []
        with open(proxy_list_path, 'r') as f:
            for line in f:
                self.proxy_list.append(line.strip())

    @classmethod
    def from_crawler(cls, crawler):
        proxy_list_path = crawler.settings.get('PROXY_LIST')
        if not proxy_list_path:
            raise NotConfigured('PROXY_LIST_PATH not provided')

        middleware = cls(proxy_list_path)
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        return middleware

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_list)
        spider.logger.info(f'Using proxy {proxy}')
        request.meta['proxy'] = f'http://{proxy}'

    def process_response(self, request, response, spider):
        spider.logger.info(f'Processing response from {response.url}')
        if response.status != 200:
            proxy = random.choice(self.proxy_list)
            request.meta['proxy'] = f'http://{proxy}'
            return request
        return response

    def spider_opened(self, spider):
        spider.logger.info('Using random proxy middleware')