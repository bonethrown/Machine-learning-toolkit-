from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from cosme.items import CosmeItem
from scrapy import log
from cosme.spiders.xpaths.xpath_registry import XPathRegistry

class Cosme(CrawlSpider):
    name = 'Lafbot'
    allowed_domains = ['laffayette.com.br']
    #might need to change this this is useless for now
    start_urls = ["http://www.laffayette.com.br/",]
    #start = ('http://www.belezanaweb.com.br/perfumes/',)
    
    deny_exts = ('site', 'include', 'ajax', 'basket', '/\d+')
    allow_exts = ('produto/[\w.-]+', 'departamento/[\w-]+')
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
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()
        self.log(str(cosmeItem),log.INFO)
        yield cosmeItem

