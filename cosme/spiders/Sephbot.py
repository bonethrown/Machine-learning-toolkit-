from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import body_or_str, get_base_url, get_meta_refresh
from scrapy.http import Request
from scrapy import log
from scrapy.contrib.loader import XPathItemLoader

from xpaths import *
import sys
from cosme.items import CosmeItem

class Cosme(CrawlSpider):
    name = 'Sbot'
    allowed_domains = ['sephora.com.br']
    #might need to change this this is useless for now
    start_urls = ["http://www.sephora.com.br"]
    #start = ('http://www.belezanaweb.com.br/perfumes/',)
    
    deny_exts = ('include', 'ajax', 'basket')
    allow_exts = (r'site/produto.asp\?idproduto=\d+',r'site/categoria.asp\?idcategoria=\d+')
        #site_rule = RWWule(SgmlLinkExtractor(), follow=True, callback='parse_item')
    rules = [
             Rule(SgmlLinkExtractor(allow = allow_exts, deny = deny_exts) , follow=True, callback='parse_item'),
             ]

   
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
        siteModulePath = "cosme.spiders.xpaths."+cosmeItem['site']
        siteModule = sys.modules[siteModulePath]
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()

        yield cosmeItem
