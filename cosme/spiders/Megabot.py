from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from cosme.items import CosmeItem

from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
from scrapy.exceptions import CloseSpider
from cosme.settings import COSME_DEBUG
from legModule import getDomain

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
    siteModule = self.xpathRegistry.getXPath(cosmeItem['site'])
    gnat = Gnat(siteModule)

    def drop(self, response):
        pass

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        cosmeItem = CosmeItem()
        cosmeItem['site'] = getDomain(response.url) 
        cosmeItem['url'] = response.url
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()

        cosmeItem['price'] = self.gnat.multiPriceExtract(cosmeItem, hxs, self.siteModule)
        cosmeItem['volume'] = self.gnat.multiVolumeExtract(cosmeItem, hxs, self.siteModule)
        if not cosmeItem['name']:
                cosmeItem['name'] = self.gnat.multiNameExtract(cosmeItem, hxs, self.siteModule)
        self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
