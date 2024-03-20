import argparse

from crawler import Crawler
from logger import logger

parser = argparse.ArgumentParser(description='Crawl a website searching for broken links')
parser.add_argument('url', help='Website URL')
parser.add_argument('--debug', action='store_true', help='Debug logs')
args = parser.parse_args()

if args.debug:
    logger.setLevel(10)
else:
    logger.setLevel(20)
    
crawler = Crawler(args.url, logger)
crawler.start()
crawler.join()