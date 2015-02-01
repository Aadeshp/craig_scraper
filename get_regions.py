#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.craigslist.org/about/sites#US")
html = r.text

soup = BeautifulSoup(html)
list = soup.find_all("a", attrs={ "name": "US" })
print(list)

