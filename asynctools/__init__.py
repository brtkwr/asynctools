"""
Various asynchronous tools
==========================

Copyright (c) 2018, Bharat Kunwar -- see attached LICENSE file
https://github.com/brtknr/asynctools
"""

from aiohttp import ClientSession, TCPConnector
from glob import glob
from PIL import Image
import traceback
import asyncio
import numpy
import os

__version__ = open(os.path.join(os.path.abspath(
	os.path.dirname(__file__)), 'VERSION')).read().strip()

class AsyncDownloader(object):
    def __init__(self, label, start_index=None, end_index=None):
        self.label = label
        os.makedirs(self.label, exist_ok=True)

        with open('{}.txt'.format(self.label)) as f:
            self.urls = f.readlines()

        self.start_index = 0
        if start_index:
            self.start_index = start_index
        
        self.end_index = len(self.urls)
        if end_index:
            self.end_index= end_index
        
        self.zfill = len(str(self.end_index))

        self.ext = { 
                'image/png': 'png',
                'image/jpeg': 'jpeg',
            }

        self.skip = set()
        for ext in self.ext.values():
            self.skip.update([os.path.basename(fname).split('.')[0] for fname in glob('{}/*.{}'.format(self.label, ext))])

        print('Skipping {} files'.format(len(self.skip)))

        self.semaphore = asyncio.Semaphore(50)
        
    async def download_url(self, url, session, index):
        retry = 0
        ctype = None
        while True:
            try:
                if index in self.skip:
                    print(index, 'Skipping')
                    return True
                else:
                    async with self.semaphore:
                        async with session.get(url) as response:
                            content = await response.read()
                            ctype = response.headers.get('content-type')
                            filename = '{}/{}.{}'.format(self.label, index, self.ext[ctype])
                            with open(filename, 'wb') as f:
                                f.write(content)
                                print(index, ctype)
                            return True
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

    async def run(self):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"}
        async with ClientSession(headers=headers, connector=TCPConnector(ssl=False)) as session:
            tasks = [asyncio.ensure_future(self.download_url(url.strip(), session, str(int(index) + self.start_index).zfill(self.zfill)))
                    for index, url in numpy.random.permutation(list(enumerate(self.urls[self.start_index:self.end_index])))]
            return await asyncio.gather(*tasks)

    def download(self):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run())
        responses = loop.run_until_complete(future)
         
        print('---\n')
        with open('{}.log'.format(self.label), 'w') as f:
            for response, url in zip(responses, self.urls):
                if response is not True:
                    print(response, url)
                    f.write('{} {}\n'.format(response, url))

        print('---\n')

class AsyncResizer(object):
    def __init__(self, label, input_format, output_format, min_size, max_ratio):
        self.label = label
        self.input_format = input_format
        self.output_format = output_format
        self.min_size = min_size
        self.max_ratio = max_ratio

        self.filepaths = glob('{}/*.{}'.format(self.label, self.input_format))

        self.resized_path = 'resized/{}'
        os.makedirs(self.resized_path.format(self.label), exist_ok=True)

        self.semaphore = asyncio.Semaphore(10)

    async def resize_image(self, filepath):
        try:
            async with self.semaphore:
                img = Image.open(filepath)
                size = img.size
                ratio = size[0]/size[1]
                if size[0] >= size[1]:
                    ratio = size[0]/size[1]
                    l0 = int(self.min_size * ratio)
                    l1 = self.min_size
                else:
                    ratio = size[1]/size[0]
                    l1 = int(self.min_size * ratio)
                    l0 = self.min_size
                print(size, (l0, l1), ratio, filepath)
                if ratio > self.max_ratio:
                    return ratio
                else:
                    assert(l0 >= self.min_size)
                    assert(l1 >= self.min_size)
                    img = img.resize((l0, l1), Image.ANTIALIAS).convert('RGB')
                    img.save(self.resized_path.format('.'.join([filepath.rsplit('.', 1)[0], self.output_format])))
                    return True
        except Exception as e:
            exception = type(e).__name__
            print(exception, filepath)
            traceback.print_exc()
            return exception

    async def run(self):
        tasks = [asyncio.ensure_future(self.resize_image(filepath)) for filepath in self.filepaths]
        return await asyncio.gather(*tasks)

    def resize(self):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run())
        responses = loop.run_until_complete(future)

        print('---\n')
        with open('{}.log'.format(self.label), 'w') as f:
            for response, filepath in zip(responses, self.filepaths):
                if response is not True:
                    print(response, filepath)
                    f.write('{} {}\n'.format(response, filepath))

        print('---\n')
