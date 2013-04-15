from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import body_or_str, get_base_url, get_meta_refresh
from scrapy.http import Request
from cosme.items import CosmeItem
from scrapy import log
from scrapy.contrib.loader import XPathItemLoader
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy.exceptions import CloseSpider
from cosme.settings import COSME_DEBUG
from xpaths import *
import sys

class Cosme(CrawlSpider):
    name = 'Zbot'
    allowed_domains = ['sepha.com.br']
    #might need to change this this is useless for now
    start_urls = ["http://www.sepha.com.br",]
    #start = ('http://www.belezanaweb.com.br/perfumes/',)
    
    deny_exts = ('site', 'include', 'ajax', 'basket')
    allow_exts = ('/cat/[\w]+([//\w.]+)')
    #for i in start:
     #   start_urls.append(i)
    #r'/bios/.\w+\.htm'
        #site_rule = RWWule(SgmlLinkExtractor(), follow=True, callback='parse_item')
    rules = [
             Rule(SgmlLinkExtractor(allow = allow_exts, deny = deny_exts) , follow=True, callback='parse_item'),
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
	#siteModulePath = "cosme.spiders.xpaths."+cosmeItem['site']
        #siteModule = sys.modules[siteModulePath]
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()
	
        yield cosmeItem
