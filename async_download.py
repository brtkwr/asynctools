#!/usr/bin/env python

from aiohttp import ClientSession
from glob import glob
import asyncio
import sys
import numpy
import os

if len(sys.argv)>1:
    URLS_FILE = sys.argv[1]
else:
<<<<<<< HEAD
    print('Usage: ./async.download.py <FILENAME.txt> <OPTIONAL: start line index> <OPTIONAL: end line index>')
=======
    print('Usage: ./async.download.py <URLS filename> <OPTIONAL: start line index> <OPTIONAL: end line index>')
>>>>>>> db68e8241fc368308a3f1318910c68d9e38e8902
    sys.exit(1)

with open(URLS_FILE) as f:
    URLS = f.readlines()

LABEL = URLS_FILE.split('.')[0]
os.makedirs(LABEL)

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
    SKIP.update([fname.split('.')[0] for fname in glob('{}/*.{}'.format(LABEL,ext))])

print('Skipping {} files'.format(len(SKIP)))

semaphore = asyncio.Semaphore(50)

async def download(url, session, index):
    try:
        if str(index) in SKIP:
            print(index, 'Skipping')
            return 'Skipping'
        else:
            async with semaphore:
                async with session.get(url) as response:
                    content = await response.read()
                    ctype = response.headers.get('content-type')
                    filename = '{}/{}.{}'.format(LABEL,str(index).zfill(ZFILL), EXT[ctype])
                    with open(filename, 'wb') as f:
                        f.write(content)
                        print(index, ctype)
                    return ctype
    except Exception as e:
        exception = type(e).__name__
        if exception == 'KeyError':
            print(index, exception, ctype, url)
        else:
            print(index, exception, url)
        return exception
 
async def run():
    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"
        }
    async with ClientSession(headers=headers) as session:
        tasks = [asyncio.ensure_future(download(URL.strip(), session, int(index) + START)) for index, URL in numpy.random.permutation(list(enumerate(URLS[START:END])))]
        return await asyncio.gather(*tasks)
 
def get_images():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run())
    return loop.run_until_complete(future)
 
responses = get_images()

with open('{}.log'.format(LABEL), 'w') as f:
    for response in responses:
        f.write('{}\n'.format(response))
