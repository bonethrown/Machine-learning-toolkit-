from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from cosme.items import CosmeItem

from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
from scrapy.exceptions import CloseSpider
from cosme.settings import COSME_DEBUG

class Cosme(CrawlSpider):
    name = 'Megabot'
    allowed_domains = ['belezanaweb.com.br']
    #might need to change this this is useless for now
    magaRegex = ".?(\/pf\/).?"
    start_urls = ["http://www.belezanaweb.com.br/perfumes/",]
    #start = ('http://www.belezanaweb.com.br/perfumes/',)
    
    deny_exts = ('=','site', 'include', 'ajax', 'basket', 'duvidas')
    allow_exts = (r'[\w\/-]+')
    denylist = ('\.asp')
    #for i in start:
    #   start_urls.append(i)
    #r'/bios/.\w+\.htm'
        #site_rule = RWWule(SgmlLinkExtractor(), follow=True, callback='parse_item')
    rules = [
             Rule(SgmlLinkExtractor(allow = allow_exts, deny = deny_exts,deny_extensions = denylist,  unique = True), follow=True, callback='parse_item'),
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
	if len(cosmeItem['price']) == 0: # Check for the 'por' price
                cosmeItem['price'] = hxs.select(siteModule.get_price_multi()).extract()
        yield cosmeItem

    def multiVolumeExtract(self, cosmeItem, hxs, siteModule):
        if  len(cosmeItem['price']) == 0:
                cosmeItem['price'] = hxs.select(siteModule.get_price_multi()).extract()
                print "*******************Second price  Check"
                print cosmeItem['price']
                return cosmeItem['price']
