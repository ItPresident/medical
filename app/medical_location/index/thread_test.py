import asyncio

import aiohttp
from datetime import datetime

start_time = datetime.now()

urls = (
    'https://likarni.com/doctors/kyev/allergologija/page/2',
    'https://likarni.com/doctors/kyev/allergologija/page/3',
    'https://likarni.com/doctors/kyev/allergologija/page/4',
)


async def fetch(session, urls):
    async with session.get(urls) as response:
        dostuffwithresponse()


async def main():
    async with aiohttp.ClientSession() as session:
        for file in list_files:
            for link in open(file).readlines():
                await fetch(session, urls)


end_time = datetime.now()
print('First Duration: {}'.format(end_time - start_time))
