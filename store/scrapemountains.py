#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Author: Brede Yabo Kristensen & Yijun Pan Stautland
##
## This script is made for collecting information from Petter's HTML page and store it in a SQLite3 database.
## If there is no SQLite3 database in the current folder, it will create a SQLite3 database from scratch.
## 
## INFO: This script is using python3 with some external packages which needs to be installed before running.
##       Please install Scrapy and CrawlSpider using pip3 install commands to install missing packages. 
##
## HOW TO USE: Use command - python3 scrapemountains.py in terminal to run this file.

# Imports for scrapy library
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import json
import os
import re
from html2text import html2text

# Imports for Sqlite3 database.
import sqlite3
import sys
import os.path
            
# Variables to store informations from HTML-sites.
# Used to parse into database.          
t_mtntable = 'mountain'
r_height = 'Height'
r_promfactor = 'PromFactor'
r_name = 'Name'
r_location = 'Location'
r_difficulty = 'Difficulty'
t_trips = 'trip'
r_mountainid = 'M_ID'
t_date = 'Date'
t_shortsummary = 'ShortSummary'
t_summary = 'Summary'

# Setting up connection to database.
# If mountains.db is not found then will make a new database called Mountains.

dbAlreadyExist = os.path.isfile('Mountains.db')

db_conn = sqlite3.connect('Mountains.db')

# If we did not find Mountains.db, create an empty database and prints a message.
if not dbAlreadyExist:
    print("Database Created")
else:
    print("Database Mountains.db found..")

theCursor = db_conn.cursor()

# Creating the tables if the mountain database is not created.
# Creating following tables: mountain, attributes, trip, resources.
if not dbAlreadyExist:
    db_conn.execute("CREATE TABLE mountain (M_ID INTEGER PRIMARY KEY AUTOINCREMENT," 
                   + "Height INTEGER," + "PromFactor INTEGER,"
	           + "Name TEXT," + "Location TEXT,"
                   + "Difficulty TEXT," + "PicAdress TEXT)")
    db_conn.execute("CREATE TABLE attributes (M_ID INTEGER," 
                    + "attribute TEXT," + "AValue TEXT," 
                    + "FOREIGN KEY(M_ID) REFERENCES mountain(M_ID))")
    db_conn.execute("CREATE TABLE trip (M_ID INTEGER," 
                    + "T_ID INTEGER PRIMARY KEY AUTOINCREMENT," + "Date TEXT," 
                    + "ShortSummary TEXT," + "Summary TEXT,"
    		    + "FOREIGN KEY(M_ID) REFERENCES mountain(M_ID))")
    db_conn.execute("CREATE TABLE resources (T_ID INTEGER," 
                    + "comments TEXT," + "address TEXT," 
                    + "FOREIGN KEY(T_ID) REFERENCES trip(T_ID))")
    db_conn.commit()

    print("Tables created!")


############################################################################################################### END DATABASE

# Script to "crawl" trough the site and save the information in variables before storing in database.
class MountainSpider(CrawlSpider):
    """Mountain spider"""

    name = "mountainspider"
    allowed_domains = ['www.ii.uib.no']
    start_urls = [
        "https://www.ii.uib.no/~petter/mountains.html"
    ]
    rules = (
        Rule(LinkExtractor(allow=('[1|10|15|20|30|40|50]00mtn\/[a-zA-Z]*\.html')), callback='parse_mountain', follow=True),
    )
    mountains = []
    mountainlist = []

    def parse_mountain(self, response):
        """ Parse data from mountain info pages """

        # Information from top table
        page = Selector(response=response)
        title = page.xpath('//h2/text()|//a/text()').extract_first() or ""
        img_url = page.xpath('//table/tr/td[2]/a/@href').extract_first() or ""
        infoTable = page.xpath('//table')

        rows = []
        for i in range(1,12):
            rows.append(infoTable.xpath('.//li[' + str(i) + ']//text()').extract_first() or "")

        # Strip unnecessary newlines
        title = title.strip('\n').strip(' ')
        rows = [ ' '.join(row.replace('\n', ' ').strip(' ').strip('.').split()) for row in rows ] 

        # Extract information
        # On those pages where name is not title, first row is title
        name = title or rows[0]
        
        # Url from response
        url = response.url

        height = ""
        pf = ""
        location = ""
        climbed = ""
        difficulty = ""
        info = []

        for row in rows: 
            height_re = re.search(r'^(\d+)[ ]*m', row)
            height_alt_re = re.search(r'^Elevation[:]? (\d+)[ ]*m', row)
            pf_re = re.search(r'factor[:]? (\d+)[ ]*m', row)
            location_re = re.search(r'Location[:]?[ ]?(.+)',row)
            climbed_re = re.search(r'Climbed[:]? (.+)',row)
            difficulty_re = re.search(r'Difficulty[:]? (.+)',row)

            if height_re:
                height = int(height_re.group(1))
            elif height_alt_re:
                height = int(height_alt_re.group(1))
            elif pf_re:
                pf = int(pf_re.group(1))
            elif location_re:
                location = location_re.group(1).replace('`', '').strip(' ')
            elif climbed_re:
                climbed = climbed_re.group(1).strip('.')
            elif difficulty_re:
                difficulty = difficulty_re.group(1).strip('.')
            elif row and row != name:
                info.append(row + '.')

        rawText = (''.join(Selector(response=response)
        .xpath('//body/text()|//body/strong|//body/p|//body/a|//body/strong/a|//body/p/a')
        .extract())
        .replace('<p></p>','')
        .replace('<strong>How to get there:</strong>','<h1>How to Get There</h1>')
        .replace('<strong>Route description:</strong>','<h1>Route Description</h1>')
        .replace('<strong>Trip report:</strong>','<h1>Trip Report</h1>')
        .replace('<strong>Comments:</strong>','<h1>Comments</h1>'))

        markdownText = html2text(rawText).replace("\n\n", '-----').replace("\n", ' ').replace('-----', "\n\n")
        
        # Database SQLqueries to store the information we just crawled down into the database tables.
        query = 'INSERT INTO {} ({}, {}, {}, {}, {}) VALUES (?, ?, ?, ?, ?)'.format(t_mtntable, r_height, r_promfactor, r_name, r_location, r_difficulty)
        query_trip = 'INSERT INTO {} ({}, {}, {}, {}) VALUES (last_insert_rowid(), ?, ?, ?)'.format(t_trips, r_mountainid, t_date, t_shortsummary, t_summary)
        theCursor.execute(query, [height, pf, name, location, difficulty])
        theCursor.execute(query_trip, [climbed, "", markdownText])


############################################################################################################### END SCRIPT

spider = MountainSpider()
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_LEVEL': 'DEBUG'
})

process.crawl(spider)
process.start()

db_conn.commit()
db_conn.close()

print("Database is now completed.")
