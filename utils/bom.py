import os
from bs4 import BeautifulSoup
import requests
import re
from string import ascii_uppercase

BASE_URL = 'http://www.boxofficemojo.com/movies/alphabetical.htm'

class BoxOfficeMojo(object):

    def __init__(self):
        self.links = []
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

    def __listing_links(self):
        return False
        # declare empty listings array
        # for each letter and include symbol page:
        #     add this page to the listings array
        #     if there is a <div class='alpha-nav-holder'>
        #         add all of those links to the listings array as well
        # return the listings array

print test_alpha_sub_links('http://www.boxofficemojo.com/movies/alphabetical.htm?letter=A&p=.htm')
