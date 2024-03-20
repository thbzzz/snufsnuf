# Snufsnuf

Snufsnuf is a simple crawler meant to find broken links on your website.

Every single link on the provided website is extracted and fetched. The resulting status code is recorded, and when the crawling is over statistics about the website's links are displayed : how many links, how many errors and detailed lists of links grouped by error status codes. 

## Installation

```console
git clone https://github.com/thbzzz/snufsnuf
cd snufsnuf
python -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

``` 
usage: snufsnuf.py [-h] [--debug] url

Crawl a website searching for broken links

positional arguments:
  url         Website URL

options:
  -h, --help  show this help message and exit
  --debug     Debug logs
```

```console
python snufsnuf.py https://thbz.fr
```

For a verbose output:

```console
python snufsnuf.py https://thbz.fr --debug
```