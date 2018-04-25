# Async tools

[![Build Status](https://travis-ci.org/brtknr/asynctools.svg?branch=master)](https://travis-ci.org/brtknr/asynctools)

- Downloader: downloads images in a list of URLs asynchronously
- Resizer: resizes images in a specified folder asynchronously

NOTE: requires Python 3.5 or above.

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
