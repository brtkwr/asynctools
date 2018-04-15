#!/usr/bin/env python

from aiohttp import ClientSession
import asyncio
import sys

if len(sys.argv)>1:
    URLS_FILE = sys.argv[1]
else:
    print('Usage: ./async.download.py <URLS FILE> <OPTIONAL:start_index> <OPTIONAL:end_index>')
    sys.exit(1)

with open(URLS_FILE) as f:
    URLS = f.readlines()

START = 0
END = len(URLS)

if len(sys.argv)>2:
    START = int(sys.argv[2])

if len(sys.argv)>3:
    END = int(sys.argv[3])

ZFILL = len(str(END))

EXT = { 
        'image/png': 'png',
        'image/jpeg': 'jpeg',
        'image/gif': 'gif',
    }

semaphore = asyncio.Semaphore(20)

async def download(URL, session, index):
    try:
        async with semaphore:
            print(index)
            async with session.get(URL) as response:
                content = await response.read()
                ctype = response.headers.get('content-type')
                filename = '{}.{}'.format(str(index).zfill(ZFILL), EXT[ctype])
                with open(filename, 'wb') as f:
                    f.write(content)
                    print(index, ctype)
                return ctype
    except Exception as e:
        exception = type(e).__name__
        if exception == 'KeyError':
            print(index, exception, ctype, URL)
        else:
            print(index, exception, URL)
        return exception
 
async def run():
    async with ClientSession() as session:
        tasks = [asyncio.ensure_future(download(URL, session, index + START)) for index, URL in enumerate(URLS[START:END])]
        return await asyncio.gather(*tasks)
 
def get_images():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run())
    return loop.run_until_complete(future)
 
responses = get_images()

with open('response.log', 'w') as f:
    for response in responses:
        f.write('{}\n'.format(response))
