#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.ii.uib.no/~petter/mountains.html')

soup = BeautifulSoup(r.text, 'html.parser')

for row in soup.find_all('table')[1].find_all('tr'):
    if len(row) > 2 and row.td.text != "#":
        cells = row.find_all('td')

        num = cells[0].text
        mountain = cells[1].text
        mountaina = cells[1].a
        height = cells[2].text
        when = cells[3].text
        comment = cells[4].text

        if mountaina != None:
            mountainurl = 'https://www.iii.uib.no/~petter/' + mountaina.get('href')
        else:
            mountainurl = ""
        
        print(mountainurl)
