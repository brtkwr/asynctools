import requests
import os
from PIL import Image
from io import BytesIO
import socket

with open('sushi.txt') as f:
    URLs = f.readlines()

with open('sushi_bad.txt') as f:
    sushi_bad = set(f.readlines())

class BadURLError(Exception):
    pass

def internet(host="1.1.1.1", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print (ex.message)
        return False
  
index = 0
for URL in URLs:
    filename = "sushi/{}.png".format(str(index).zfill(6))
    try:
        if URL in sushi_bad:
            raise BadURLError('PIL was unable to download from this URL', URL)
        if not os.path.exists(filename):
            img = Image.open(BytesIO(requests.get(URL).content))
            img.save(filename)
        else:
            print('Skipping',filename)
        print(filename, end='\r')
        index += 1
    except Exception as e:
        expName = type(e).__name__
        if expName == 'ConnectionError':
            if not internet():
                raise e
            with open('sushi_bad.txt','a') as f:
                f.write(URL)
            sushi_bad.add(URL)
            print(e)
