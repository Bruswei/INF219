#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

class MountainSpider(CrawlSpider):
    """Mountain spider"""

    name = "mountainspider"
    allowed_domains = ['www.ii.uib.no']
    start_urls = [
        "https://www.ii.uib.no/~petter/mountains.html"
    ]

    rules = (
        Rule(LinkExtractor(allow=('mountains.html')), callback='parse_table'),
        Rule(LinkExtractor(allow=('5000mtn\/')), callback='parse_mountain'),
        Rule(LinkExtractor(allow=('4000mtn\/')), callback='parse_mountain'),
        Rule(LinkExtractor(allow=('3000mtn\/')), callback='parse_mountain'),
        Rule(LinkExtractor(allow=('2000mtn\/')), callback='parse_mountain'),
        Rule(LinkExtractor(allow=('1500mtn\/')), callback='parse_mountain'),
        Rule(LinkExtractor(allow=('1000mtn\/')), callback='parse_mountain'),
        Rule(LinkExtractor(allow=('100mtn\/')), callback='parse_mountain'),
    )

    def parse_table(self, response):
        """ Parse mountain table from front page """
        # Mountain table is the second table on the website
        mountainTable = Selector(response=response).xpath('//table[1]/tr')

        for rownum, row in enumerate(mountainTable):
            # The rows we are interested in are row 3 to 1351
            if rownum > 2 and rownum < 1352: 
                number = row.xpath('.//td[1]/text()').extract_first()
                name = row.xpath('.//td[2]/text()').extract_first()
                url = row.xpath('.//td[2]/a/@href').extract_first()
                height = row.xpath('.//td[3]/text()').extract_first()
                when = row.xpath('.//td[4]/text()').extract_first()
                comment = row.xpath('.//td[5]/text()').extract_first()

                print("NUMBER   | {}".format(number))
                print("NAME     | {}".format(name))
                print("URL      | {}".format(url))
                print("HEIGHT   | {}".format(height))
                print("WHEN     | {}".format(when))
                print("COMMENT  | {}".format(comment))

    def parse_mountain(self, response):
        """ Parse data from mountain info pages """
        # Information from top table
        infoTable = Selector(response=response).xpath('//table/tr')
        name = infoTable.xpath('.//td[1]/a/h2/text()').extract_first()
        height = infoTable.xpath('.//td[1]/ul/li[2]/text()').extract_first()
        pf = infoTable.xpath('.//td[1]/ul/li[3]/text()').extract_first()
        location = infoTable.xpath('.//td[1]/ul/li[4]/text()').extract_first()
        gps = infoTable.xpath('.//td[1]/ul/li[5]/text()').extract_first()
        climbed = infoTable.xpath('.//td[1]/ul/li[6]/text()').extract_first()
        difficulty = infoTable.xpath('.//td[1]/ul/li[7]/text()').extract_first()

        # Strip unnecessary newlines
        name = name.strip('\n') if name != None else None
        height = height.strip('\n') if height != None else None
        pf = pf.strip('\n') if pf != None else None
        location = location.strip('\n') if location != None else None
        gps = gps.strip('\n') if gps != None else None
        climbed = climbed.strip('\n') if climbed != None else None
        difficulty = difficulty.strip('\n') if difficulty != None else None

        # Select text straight in body node, strong tags right under body node, and p tags 
        # right under body node in DOM
        rawText = Selector(response=response).xpath('//body/text()|//body/strong/text()|//body/p//text()').extract()
        # Replace newlines with spaces, remove strange \xa0 characters, and replace multiple 
        # consecutive spaces with one space character
        strippedText = [ ' '.join(s.replace('\n', ' ').replace('\xa0', '').split()) for s in rawText ]

        # Filter empty strings
        informationText = list(filter(None, strippedText))

        print("NAME       | {}".format(name))
        print("HEIGHT     | {}".format(height))
        print("PF         | {}".format(pf))
        print("LOCATION   | {}".format(location))
        print("GPS        | {}".format(gps))
        print("CLIMBED    | {}".format(climbed))
        print("DIFFICULTY | {}".format(difficulty))
        print("INFO | {}".format(informationText))

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MountainSpider)
process.start()
        
