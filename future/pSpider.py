import json, urllib2
from cosme.pipes import pipeMethods
from  pipes.utils import db,utils, itemTools, db2
from cosme import dataOps
from cosme.dataOps import nameGen
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.crawler import Crawler


class PythonSpider(Spider):
        name = 'hoss'

        def parse(self, response):
                print 'yes'
                return response
        #### START URLS ####
        def start_requests(self):
                for item in self.start_urls:
                        yield self.make_requests_from_url(item['url'])


