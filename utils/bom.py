import os
from bs4 import BeautifulSoup
import requests
import re
from string import ascii_uppercase

BASE_URL = 'http://www.boxofficemojo.com/movies/alphabetical.htm'

class BoxOfficeMojo(object):

    def __init__(self):
        self.links = []
        self.listing_links = self.__get_listing_links()
        page_links = self.__get_movie_links(BASE_URL)
        self.links.extend(page_links)

    def collect_movie_links(self):
        for l in self.listing_links:
            self.links.extend(self.__get_movie_links(l))

    def __get_movie_links(self,url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')
        links = []

        a = soup.find_all(href = re.compile('\/movies\/\?id'))
        for l in a:
            link = 'http://www.boxofficemojo.com' + l['href']
            links.append(link)
        return links

    def __alpha_sub_links(self,url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')
        links = []

        alpha_links = soup.find('div','alpha-nav-holder').find_all('a')
        for l in alpha_links:
            links.append(l['href'])
        return links

    def __get_listing_links(self):
        links = []
        for c in ascii_uppercase:
            base_link = 'http://www.boxofficemojo.com/movies/alphabetical.htm?letter=' + c + '&p=.htm'
            links.append(base_link)
            for l in self.__alpha_sub_links(base_link):
                links.append('http://www.boxofficemojo.com' + l)
        return links

    def __scrape_film_page(self,url):
        '''Requires a Box Office Mojo url leading to the detail page of a film.
        '''
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')

        title = soup.find_all(face='Verdana')[1].b.text
        genre = soup.find_all(string=re.compile('Genre'))[1].find_next_sibling().text
        runtime = soup.find_all(string=re.compile('Runtime'))[0].find_next_sibling().text
        release = soup.find_all(string=re.compile('Release Date'))[0].find_next_sibling().text
        try:
            domestic = soup.find_all(string=re.compile('Domestic Total Gross'))[0].find_next_sibling().text
        except IndexError:
            domestic = 'Unknown'

        return { 'title':title, 'genre':genre, 'runtime':runtime, 'release':release, 'domestic':domestic }
