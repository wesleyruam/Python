import requests
from bs4 import BeautifulSoup as bs4
import logging
from urllib.parse import urljoin
import validators
from urllib.parse import urlparse
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(name)s %(message)s')
logger = logging.getLogger("[LOG]")

class ExtractLinks:
    def __init__(self, url):
        self.url = url
        self.find_directories = list()
        self.processed_links = set()

    def _getHTMLfromURL(self, path=''):
        try:
            if path == '':
                r = requests.get(self.url)
            else:
                url_full = urljoin(self.url, path)
                r = requests.get(url_full)

            if r.status_code == 200:            
                logger.info(f'{r.url} - {r.status_code}')
                soup = bs4(r.text, 'html.parser')
                self._getLinksFromHTML(soup)
            else:
                self._requestNewsLink()
        except Exception as e:
            print(f"Erro1: {e}")

    def _requestNewsLink(self):
        try:
            if self.find_directories:
                link = self.find_directories.pop(0)
                url_full = urljoin(self.url, link)
                if url_full not in self.processed_links:
                    self.processed_links.add(url_full)
                    self.url = url_full
                    self._getHTMLfromURL(link)
                else:
                    self._requestNewsLink()
            else:
                print('Todos os links foram processados.')
        except Exception as e:
            print(f'Erro ao processar novo link: {e}')

    def _getLinksFromHTML(self, soup: bs4):
        try:
            for link in soup.find_all('a'):
                if link.get('href') is None:
                    continue

                if not link.get('href').startswith(('mailto')):
                    new_link = link.get('href')
                    full_link = urljoin(self.url, new_link)
                    parsed_full_link = urlparse(full_link)

                    if validators.url(new_link):
                        parsed_url_link = urlparse(new_link)
                        parsed_url = urlparse(self.url)
                        
                        url_link = f'{parsed_url_link.scheme}://{parsed_url_link.netloc}'
                        url = f'{parsed_url.scheme}://{parsed_url.netloc}'
                        caminho = parsed_url_link.path

                        if url == url_link and caminho != "/":
                            if url_link == url: 
                                if caminho not in self.find_directories:
                                    self.find_directories.append(caminho)
                    else:
                        if parsed_full_link.path not in self.find_directories:
                            self.find_directories.append(parsed_full_link.path)

            self._requestNewsLink()
        except Exception as e:
            print(f'Erro ao processar links do HTML: {e}')

    def start(self):
        self._getHTMLfromURL()
        print(self.processed_links)

r = ExtractLinks("http://testphp.vulnweb.com/").start()
