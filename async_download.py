#!/usr/bin/env python

from aiohttp import ClientSession, TCPConnector
from glob import glob
import traceback
import asyncio
import sys
import numpy
import os

if len(sys.argv)>1:
    URLS_FILE = sys.argv[1]
else:
    print('Usage: ./async_download.py <FILENAME.txt> <OPTIONAL: start line index> <OPTIONAL: end line index>')
    sys.exit(1)

with open(URLS_FILE) as f:
    URLS = f.readlines()

LABEL = URLS_FILE.split('.')[0]
os.makedirs(LABEL, exist_ok=True)

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

SKIP = set()
for ext in EXT.values():
    SKIP.update([os.path.basename(fname).split('.')[0] for fname in glob('{}/*.{}'.format(LABEL,ext))])

print('Skipping {} files'.format(len(SKIP)))

semaphore = asyncio.Semaphore(50)

async def download(url, session, index):
    retry = 0
    ctype = None
    while True:
        try:
            if index in SKIP:
                print(index, 'Skipping')
                return 'Skipping'
            else:
                async with semaphore:
                    async with session.get(url) as response:
                        content = await response.read()
                        ctype = response.headers.get('content-type')
                        filename = '{}/{}.{}'.format(LABEL, index, EXT[ctype])
                        with open(filename, 'wb') as f:
                            f.write(content)
                            print(index, ctype)
                        return ctype
        except Exception as e:
            exception = type(e).__name__
            print(index, ctype, exception, retry, url)
            if exception == 'ClientConnectorError':
                retry += 1
                if retry < 3:   
                    await asyncio.sleep(3)
                else:
                    traceback.print_exc()
                    return exception
            else:
                traceback.print_exc()
                return exception 

async def run():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"}
    async with ClientSession(headers=headers, connector=TCPConnector(ssl=False)) as session:
        tasks = [asyncio.ensure_future(download(URL.strip(), session, str(int(index) + START).zfill(ZFILL)))
                for index, URL in numpy.random.permutation(list(enumerate(URLS[START:END])))]
        return await asyncio.gather(*tasks)

def get_images():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run())
    return loop.run_until_complete(future)
 
responses = get_images()

with open('{}.log'.format(LABEL), 'w') as f:
    for response in responses:
        f.write('{}\n'.format(response))
