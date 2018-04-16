# Description

Downloads list of image URLs in a file asynchronously using Python3

# Installation

After cloning,

```
cd async_download
virtualenv -p python3 .
pip install -U pip
pip install -r requirements.txt
```

# Usage



```
./async_download.py <FILENAME.txt> <OPTIONAL: start line index> <OPTIONAL: end line index>

e.g.
./async_download.py urls.txt
./async_download.py urls.txt 10000
./async_download.py urls.txt 10000 20000
```
