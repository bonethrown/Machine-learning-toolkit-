from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
from superSpider import Gnat
import re
 
class Cosme(CrawlSpider):
    

    name = 'Sbot'
    allowed_domains = ["sephora.com.br"]
    denydom = ["centralderelacionamento.sephora.com.br", "ilovebeauty.sephora.com.br", "nossaslojas.sephora.com.br", "seguro.sephora.com.br",'busca.sephora.com.br']
    #might need to change this this is useless for now
    
    start_urls = ["http://www.sephora.com.br/perfumes",
		"http://www.sephora.com.br/maquiagem",
		"http://www.sephora.com.br/cabelos",
		"http://www.sephora.com.br/perfumes",
		"http://www.sephora.com.br/maquiagem",
		"http://www.sephora.com.br/tratamento",
		"http://www.sephora.com.br/corpo-e-banho",
		"http://www.sephora.com.br/presentes",
		"http://busca.sephora.com.br/resultado.aspx?orderby=desconto"]
	
    deny_1 = re.compile(r'(?=.*(login|asp|newsletter|php|busca|include|basket|cesta|view=all|comprar|compartilhe|avise-me|produtoDetalhe|aspx|ajax)).*', re.I)
	
    rules = [
             Rule(SgmlLinkExtractor(deny = deny_1, deny_domains = denydom, allow_domains = allowed_domains,  unique = True) , follow=True, callback='parse_item'),
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
		cosmeItem[field] = hxs.xpath(siteModule.META[field]).extract()
        #cosmeItem['price'] = gnat.multiPriceExtract(cosmeItem, hxs)
        #cosmeItem['volume'] = gnat.multiVolumeExtract(cosmeItem, hxs)
        #if not cosmeItem['name']:
         #       cosmeItem['name'] = gnat.multiNameExtract(cosmeItem, hxs)
        #self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
        
