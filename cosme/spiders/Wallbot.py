from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
from superSpider import Gnat

 
class Cosme(CrawlSpider):
    

    name = 'Walbot'
    allowed_domains = ["walmart.com.br"]
    denydom = ["centralderelacionamento.sephora.com.br", "ilovebeauty.sephora.com.br", "nossaslojas.sephora.com.br", "seguro.sephora.com.br"]
    #might need to change this this is useless for now
    
    start_urls = ["http://www.walmart.com.br/departamento/beleza-e-saude/1","http://www.sephora.com.br/maquiagem","http://www.sephora.com.br/cabelos"]
    #start_urls = ['http://www.sephora.com.br/site/produto.asp?idproduto=13943']
    allow_exts =(r'\/produto\/Beleza-e-Saude\/([\/\w \.-]*)*\/?$', r'\/categoria/beleza-e-saude\/([\/\w \.-]*)*\/?$', ) 
    deny_exts = (r'\/produto\/Beleza-e-Saude\/Massageador\/([\/\w \.-]*)*\/?$', r'')
        #site_rule = RWWule(SgmlLinkExtractor(), follow=True, callback='parse_item')
    rules = [
             Rule(SgmlLinkExtractor(deny_domains = denydom, allow_domains = allowed_domains,  unique = True) , follow=True, callback='parse_item'),
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
   	gnat = Gnat(siteModule) 
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()

        cosmeItem['price'] = self.gnat.multiPriceExtract(cosmeItem, hxs, self.siteModule)
        cosmeItem['volume'] = self.gnat.multiVolumeExtract(cosmeItem, hxs, self.siteModule)
        if not cosmeItem['name']:
                cosmeItem['name'] = self.gnat.multiNameExtract(cosmeItem, hxs, self.siteModule)
        self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
        
