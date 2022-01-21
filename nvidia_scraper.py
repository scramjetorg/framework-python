from scramjet.streams import Stream
from pyppeteer import launch

import asyncio
import requests

# color codes for pretty output
grey="\033[37m"
strong="\033[97;1m"
reset="\033[0m"

params = {
    'skus': 'DE',
    'locale': 'DE'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-GB',
    'Origin': 'https://shop.nvidia.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://shop.nvidia.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers',
}

# Simple Nvidia page scraper
async def simple_nvidia_scraper_example() -> None:
    data = requests.get("https://api.store.nvidia.com/partner/v1/feinventory", params=params, headers=headers).json()
    urls = await (
        Stream
            .read_from(data.get('listMap'))
            .filter(lambda x: x.get('is_active') == 'true')
            .map(lambda x: x.get('product_url'))
            .to_list()
    )
    browser = await launch(
        headless=False,
        autoClose=False
    )
    pages = await browser.pages()

    for idx, url in enumerate(urls):
        await pages[idx].goto(url)
        if len(pages) < len(urls):
            pages.append(await browser.newPage())
        

print(f"\n{strong}Running simple_stream_example:{reset}")
asyncio.run(simple_nvidia_scraper_example())
