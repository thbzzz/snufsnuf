from threading import Thread
from urllib.parse import urljoin

import colorama
from bs4 import BeautifulSoup

from logger import logger
from utils import GracefulKiller, HttpClient


class Crawler(Thread):
    """Thread taking a website URL as parameter to crawl it extracting all links.
    Searches for dead links such as 404.
    """    
    def __init__(self, base_url: str, logger):
        """Crawler init.

        Args:
            base_url (str): Website to scan.
            logger (logging.Logger): Logger.
        """        
        super(Crawler, self).__init__()

        self._id = id
        self.base_url = base_url
        self.logger = logger
                
        self.http_client = HttpClient(self.logger)
        self.killer = GracefulKiller(self.logger)
        
        self.links = {}
        self.buffer = [self.base_url]

    def run(self):
        """Crawling main loop. Pop URLs from the buffer and feed it with extracted links."""
        self.logger.info('Crawling started')
        while not self.killer.kill_now:
            # If the buffer is empty, work is done
            if len(self.buffer) == 0:
                self.logger.info('Crawling ended')
                break

            # Get new URL from buffer
            self.url = self.buffer.pop()
            
            # Skip URL if already buffered or fetched
            if self.url in self.links.keys() or self.url in self.buffer:
                continue
            
            # Fetch URL and record status code
            if (webpage := self.http_client.get(self.url)) == None:
                self.links[self.url] = 0
                continue

            self.links[self.url] = webpage.status_code

            if not webpage.ok:
                self.logger.warning(f'{colorama.Fore.CYAN}{self.url}{colorama.Style.RESET_ALL} {colorama.Fore.YELLOW}{webpage.status_code}{colorama.Style.RESET_ALL}')
                continue

            # Bufferize page links if the page is part of base website
            if self.url.startswith(self.base_url):
                links = self.extract_links(webpage)
                
                for link in links:
                    if link not in self.links.keys() and link not in self.buffer:
                        self.buffer.insert(0, link)
        
        # Display the results
        self.display()

    def display(self):
        """Log collected statistics about the fetched links."""
        status_codes = set(self.links.values())
        
        self.logger.debug(f'Links: {self.links}')
        self.logger.debug(f'Status codes: {status_codes}')

        nb_links = len(self.links.keys())
        if 200 in status_codes:
            nb_ok = len([l for l in self.links.keys() if self.links[l] == 200])
            status_codes.remove(200)
        else:
            nb_ok = 0
        nb_errors = nb_links - nb_ok
        
        # Log total fetched links
        self.logger.info(f'{colorama.Style.BRIGHT}Total links: {colorama.Fore.CYAN}{nb_links}{colorama.Style.RESET_ALL}')
        # Log total errors and status codes not ok
        self.logger.info(f'{colorama.Style.BRIGHT}Total errors: {colorama.Fore.RED}{nb_errors}{colorama.Style.RESET_ALL}')
        # Log URLs for each status code
        for code in sorted(status_codes, key=lambda x: len([l for l in self.links.keys() if self.links[l] == x]), reverse=True):
            links = [l for l in self.links.keys() if self.links[l] == code]
            
            # Replace ambiguous '0' which is not really a status code
            if code == 0:
                code = 'Connection'
            
            self.logger.info(f'\\_ {colorama.Style.BRIGHT}{code}{colorama.Style.RESET_ALL}: {colorama.Fore.RED + colorama.Style.BRIGHT}{len(links)}{colorama.Style.RESET_ALL}')
            for link in sorted(links, key=lambda x: x.startswith(self.base_url), reverse=True):
                self.logger.info(f'  \\_ {link}')

    def extract_links(self, webpage: str) -> list[str]:
        """Extract links from a webpage.

        Args:
            webpage (str): Webpage HTML code.

        Returns:
            list[str]: List of extracted links.
        """
        try:
            soup = BeautifulSoup(webpage.content.decode('utf-8'), 'html.parser')
        except UnicodeDecodeError:
            soup = BeautifulSoup(webpage.text, 'html.parser')
        links = []

        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                # Don't extract anchors, Javascript, mailto, etc. links
                if not any([
                    link['href'].startswith('#'),
                    link['href'].startswith('javascript:'),
                    link['href'].startswith('mailto:'),
                ]):
                    links.append(urljoin(self.url, link['href']))

        return links