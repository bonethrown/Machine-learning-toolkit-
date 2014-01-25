from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
#from superSpider import Gnat
from superSpider import PartialCrawler
import re

class Cosme(CrawlSpider):
    

    name = 'Subbot'
    allowed_domains = ["submarino.com.br"]
    #might need to change this this is useless for now
    part = PartialCrawler()
    re_allow = part.construct()

	    	
    start_urls = ["http://www.submarino.com.br/loja/259977/perfumaria", "http://www.submarino.com.br/linha/293730/perfumaria/corpo", "http://www.submarino.com.br/linha/335240/perfumaria/esmaltes"]

    den = re.compile(r'http://www.submarino.com.br((?=.*\/)(?!.*(offset|produto)).*)', re.I)
    den_1 = re.compile(r'((?=.*(order|limit)).*)', re.I)

    deny_list = [den, den_1]
    		
    rules = [
             Rule(SgmlLinkExtractor(allow_domains = allowed_domains,deny = deny_list, allow = re_allow, unique = True), follow=True, callback='parse_item')
             ]

    xpathRegistry = XPathRegistry()
        
    def getDomain(self, url):
        try:
            urlSeg = url.split('/')
            domain = urlSeg[2]
            segDom = domain.split('.')
            if segDom[1]=='com':
                return segDom[0]
            else:
                return segDom[1]
        except:
                return ""

    def drop(self, response):
        pass

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        cosmeItem = CosmeItem()
        cosmeItem['site'] = self.getDomain(response.url)
        cosmeItem['url'] = response.url
    	siteModule = self.xpathRegistry.getXPath(cosmeItem['site'])
   	#gnat = Gnat(siteModule) 
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()

        #cosmeItem['price'] = self.gnat.multiPriceExtract(cosmeItem, hxs, self.siteModule)
        #cosmeItem['volume'] = self.gnat.multiVolumeExtract(cosmeItem, hxs, self.siteModule)
        #if not cosmeItem['name']:
         #       cosmeItem['name'] = self.gnat.multiNameExtract(cosmeItem, hxs, self.siteModule)
        #self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
        
