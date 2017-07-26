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
