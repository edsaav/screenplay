import os
from bs4 import BeautifulSoup
import requests
import re
from string import ascii_lowercase

BASE_URL = 'http://www.boxofficemojo.com/movies/alphabetical.htm'

class BoxOfficeMojo(object):

    def __init__(self):
        self.links = []
