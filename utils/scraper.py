import os
from bs4 import BeautifulSoup
import requests
import re
from string import ascii_lowercase

SCRIPTS_FOLDER = 'scripts'

class Scraper(object):

    def __init__(self):
        self.links = []
        for c in ascii_lowercase:
            url = 'http://www.imsdb.com/alphabetical/' + c
            page_links = self.__get_imsdb_links(url)
            self.links.extend(page_links)

    def capture(self, url):
        text = self.pull(url)
        if text:
            url_suffix = url.split('/')[-1]
            file_name = re.sub('.html', '.txt', url_suffix)
            with open(os.path.join(SCRIPTS_FOLDER, file_name), 'w') as doc:
                doc.write(text.encode('ascii', 'ignore'))

    def pull(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')
        if soup.find('td', { 'class' : 'scrtext' }):
            content = soup.find('td', { 'class' : 'scrtext' }).text
            return content.split('   THE END')[0]

    def __get_imsdb_links(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')
        links = []

        a = soup.find_all(href = re.compile('\/Movie'))
        for l in a:
            c = l['href'].split('/')[2].split(' ')[:-1]
            link = 'http://www.imsdb.com/scripts/' + re.sub(':', '', '-'.join(c)) + '.html'
            links.append(link)
        return links

#get_imsdb_links('http://www.imsdb.com/alphabetical/A')
s = Scraper()
for n in range(101,len(s.links)):
    s.capture(s.links[n])
