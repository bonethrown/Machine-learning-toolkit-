from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import body_or_str, get_base_url, get_meta_refresh
from scrapy.http import Request
from cosme.items import CosmeItem
from scrapy import log
from scrapy.contrib.loader import XPathItemLoader
import re
from xpaths import *
import sys
from cosme.spiders.xpaths.xpath_registry import XPathRegistry

#TODO Use SitemapSpider instead for magazineluiza.com.br
class Cosme(CrawlSpider):

    name = 'Infbot'
    allowed_domains = ['infinitabeleza.com.br']   #Add one by one, comment out as necassary
 
    #magaRe = re.compile('.?(\/pf\/pfba\/)$')
    #allowed_domains = ['pornhub.com']
    start_urls = ["http://www.infinitabeleza.com.br/shampoo-ct-37-238722.htm",
		"http://www.infinitabeleza.com.br/ofertas-ct-169-238722.htm",
		"http://www.infinitabeleza.com.br/condicionador-ct-49-238722.htm",
		"http://www.infinitabeleza.com.br/mascaras-ct-60-238722.htm",
		"http://www.infinitabeleza.com.br/tratamento-p-cabelos-ct-152-238722.htm",
		"http://www.infinitabeleza.com.br/leavein-ct-120-238722.htm",
		"http://www.infinitabeleza.com.br/finalizadores-ct-114-238722.htm",
		"http://www.infinitabeleza.com.br/relaxamentos-alisamentos-ct-94-238722.htm",
		"http://www.infinitabeleza.com.br/linha-masculina-ct-158-238722.htm",
		"http://www.infinitabeleza.com.br/maquiagem-ct-116-238722.htm",
		"http://www.infinitabeleza.com.br/unhas-ct-188-238722.htm",
		"http://www.infinitabeleza.com.br/corpo-e-banho-ct-85-238722.htm",
		"http://www.infinitabeleza.com.br/acessorios-e-equipamentos-ct-89-238722.htm"]

    #TODO put these in a file!i
    deny_1 = re.compile('^((?=.*(login|signup|photos|login|loja)).*)$', re.I)

    magazine_rule = Rule(SgmlLinkExtractor(unique=True,deny=deny_1 ),callback='parse_item',follow=True)
   
   
    rules = (
	magazine_rule,
		)

    xpathRegistry = XPathRegistry()
    
    #not used for now, we will crawl all links
    def drop(self,response):
        pass
    
    #Warning this is very Naive will only work with http://www.foobar.com/ type domains
    def getDomain(self,url):
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
        
    def parse_item(self, response):

        #Lets try using ItemLoaders built into scrapy
        #l = XPathItemLoader(item=CosmeItem(),response=response)

        x = HtmlXPathSelector(response)
        cosmeItem = CosmeItem()
        
        cosmeItem['site']= self.getDomain(response.url)
        cosmeItem['url'] = response.url
        cosmeItem['volume'] = ""
	cosmeItem['sku'] = ""

	#Get xpaths that correspond to our domain
        siteModule = self.xpathRegistry.getXPath(cosmeItem['site'])        
        
        #Traverse All our fields in our xpath
        for field in siteModule.META.keys():
            cosmeItem[field] = x.select(siteModule.META[field]).extract()
        
        yield cosmeItem
