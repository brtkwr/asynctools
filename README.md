# Description

Downloads list of image URLs in a file asynchronously using Python3

# Installation

After cloning,

```
cd asynctools
virtualenv -p python3 .
pip install .
```

# Usage


## Downloader
```
download_async <LABEL> <OPTIONAL: start line index> <OPTIONAL: end line index>

e.g.
download_async urls
download_async urls 10000
download_async urls 10000 20000
```

## Resizer
```
resize_async <LABEL> <INPUT_FORMAT> <OUTPUT FORMAT> <MIN SIZE> <MAX RATIO>

e.g.
resize_async urls jpeg jpeg 300 2.0
```
