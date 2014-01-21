from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
from superSpider import Gnat

 
class Cosme(CrawlSpider):
    

    name = 'Sbot'
    allowed_domains = ["sephora.com.br"]
    denydom = ["centralderelacionamento.sephora.com.br", "ilovebeauty.sephora.com.br", "nossaslojas.sephora.com.br", "seguro.sephora.com.br",'busca.sephora.com.br']
    #might need to change this this is useless for now
    
    start_urls = ["http://www.sephora.com.br/perfumes","http://www.sephora.com.br/maquiagem","http://www.sephora.com.br/cabelos"]
    #start_urls = ['http://www.sephora.com.br/site/produto.asp?idproduto=13943']
    #allow_exts =(r'site/produto\.asp\?id=\d+', r'imagens[\w\./{}-]+',r'site/categoria\.asp\?\w+=\d+', r'site/marca\.asp\?\w+=\d+', r'site/departamento\.asp\?\w+=\d+') 
    deny_exts = (r'checkout\.asp', r'login\.asp', r'newsletter\.asp',r'\.php',r'busca', r'mac', r'include', r'ajax', r'basket\.asp', r'cesta\.asp',r'comprar\.asp', r'view=all', r'compartilhe\.asp', r'marca\.asp\?[\w&=]+', r'avise-me\.asp\?id=\d+', r'produtoDetalhe\.asp')
   # allow_exts = (r'produto.asp\?idproduto=\d+')
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

        #cosmeItem['price'] = gnat.multiPriceExtract(cosmeItem, hxs)
        #cosmeItem['volume'] = gnat.multiVolumeExtract(cosmeItem, hxs)
        #if not cosmeItem['name']:
         #       cosmeItem['name'] = gnat.multiNameExtract(cosmeItem, hxs)
        self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
        
