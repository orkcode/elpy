import sys
import os
import json
import random
import time
import asyncio
import aiohttp
from contextlib import contextmanager, asynccontextmanager
import xml.etree.ElementTree as ET
from aiolimiter import AsyncLimiter

async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


@asynccontextmanager
async def allocate_proxy():
    """Get a free proxy and hold it as in use"""
    available_proxies = [p for p in proxy_list if p not in proxies_in_use]
    if available_proxies:
        proxy = random.choice(available_proxies)
    else:
        proxy = random.choice(proxy_list)
    try:
        proxies_in_use.append(proxy)
        yield f"http://{proxy}"  # Ensure the proxy URL is correctly formatted
    finally:
        proxies_in_use.remove(proxy)


MAX_REQUESTS_PER_MINUTE = 250
limiter = AsyncLimiter(MAX_REQUESTS_PER_MINUTE, 60)
PARALLEL_REQUESTS = 50
results = []
proxies_in_use = []

with open("./proxies.txt") as f:
    proxy_list = [line.strip() for line in f.readlines()]


async def fetch(url: str, session: aiohttp.ClientSession, use_proxy: object = proxy_list):
    async with limiter:
        if use_proxy:
            async with allocate_proxy() as proxy:
                try:
                    async with session.get(url, proxy=proxy, timeout=1) as response:
                        print(f'Fetched url {url} with proxy {proxy}')
                        return await response.text()
                except Exception as e:
                    print(f'Failed to fetch url {url} with proxy {proxy} due to {e}')
        else:
            try:
                async with session.get(url, timeout=1) as response:
                    print(f'Fetched url {url} without proxy')
                    return await response.text()
            except Exception as e:
                print(f'Failed to fetch url {url} without proxy due to {e}')


async def fetch_xml(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            xml_content = await fetch(url, session)
            print(f"XML fetched successfully")
            print(ET.fromstring(xml_content))
            return ET.fromstring(xml_content)
    except Exception as e:
        print(f"Error fetching XML: {e}")
        return None


async def fetch_all(urls: list[str]):
    conn = aiohttp.TCPConnector(limit_per_host=5, limit=0, ttl_dns_cache=300, ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [fetch(url, session) for url in urls]
        return await gather_with_concurrency(PARALLEL_REQUESTS, *tasks)


async def parse_and_fetch():
    url = 'https://www.promelec.ru/sitemap/Goods.xml'
    root = await fetch_xml(url)
    if root is not None:
        # Use the namespace in the findall function
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [elem.text for elem in root.findall('.//sitemap:url/sitemap:loc', namespace)]
        print(f'Found {len(urls)} links in sitemap')


    start = time.time()
    await fetch_all(urls)
    end = time.time()
    print(f'download {len(urls)} links in {end - start} seconds')


asyncio.run(parse_and_fetch())
