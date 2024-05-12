import requests

cookies = {
    '__ddg1_': 'gFjOzQ1wIvIrXZZsymQ9',
    '_ga_LY608YRQ43': 'GS1.1.1715263269.7.1.1715264555.0.0.0',
    '_ga': 'GA1.1.980556295.1707600649',
    '_ga_285H1KH84C': 'GS1.1.1715263269.14.1.1715264555.0.0.0',
    '_ga_1YKJ0EPJBW': 'GS1.1.1715263269.14.1.1715264555.0.0.0',
    '_ymab_param': '_dpfFjRVaRk3wfGUcZc1Y-jsTuLiChULCH_-tXLBgwLm0VlgyHMypNlaU9jxipR2F6yfSby6637eUL5Is2dFfO89HCQ',
    '_ym_uid': '1707612343687129948',
    '_ym_d': '1707612343',
    'basket': '4354e766c7e75079ed02a05167392e4e26857179d63392e801a00ab5f41219b0a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22basket%22%3Bi%3A1%3Bi%3A18883156%3B%7D',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '__ddgid_': 'vT5aT1YKfh9tJowN',
    '__ddgmark_': 'AIgESgC3XmAeMbH8',
    '__ddg5_': 'uBXD1tLVRIEYwyku',
    '__ddg2_': 'Ts76MbOFQrVKbRCY',
    '_frontendSessionId': 'ccb414118b1ac8a8e12cd47af6c9d761',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.promelec.ru',
    'Connection': 'keep-alive',
    'Referer': 'https://www.promelec.ru/product/163799/',
    # 'Cookie': '__ddg1_=gFjOzQ1wIvIrXZZsymQ9; _ga_LY608YRQ43=GS1.1.1715263269.7.1.1715264555.0.0.0; _ga=GA1.1.980556295.1707600649; _ga_285H1KH84C=GS1.1.1715263269.14.1.1715264555.0.0.0; _ga_1YKJ0EPJBW=GS1.1.1715263269.14.1.1715264555.0.0.0; _ymab_param=_dpfFjRVaRk3wfGUcZc1Y-jsTuLiChULCH_-tXLBgwLm0VlgyHMypNlaU9jxipR2F6yfSby6637eUL5Is2dFfO89HCQ; _ym_uid=1707612343687129948; _ym_d=1707612343; basket=4354e766c7e75079ed02a05167392e4e26857179d63392e801a00ab5f41219b0a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22basket%22%3Bi%3A1%3Bi%3A18883156%3B%7D; _ym_isad=2; _ym_visorc=w; __ddgid_=vT5aT1YKfh9tJowN; __ddgmark_=AIgESgC3XmAeMbH8; __ddg5_=uBXD1tLVRIEYwyku; __ddg2_=Ts76MbOFQrVKbRCY; _frontendSessionId=ccb414118b1ac8a8e12cd47af6c9d761',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # 'Content-Length': '0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

params = {
    'id': '37127',
}

response = requests.get(
    'https://www.promelec.ru/product/163799/',
)
print(response.text)