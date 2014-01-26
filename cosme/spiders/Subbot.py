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

	    	
    start_urls = ["http://www.submarino.com.br/sublinha/293668/perfumaria/perfumes/perfume-feminino",
		"http://www.submarino.com.br/sublinha/293609/perfumaria/perfumes/perfume-masculino",
		"http://www.submarino.com.br/sublinha/293688/perfumaria/perfumes/perfume-unissex",
		"http://www.submarino.com.br/sublinha/356112/perfumaria/perfumes/estojos-e-kits",

		"http://www.submarino.com.br/linha/293728/perfumaria/olhos",
		"http://www.submarino.com.br/linha/293589/perfumaria/labios",
		"http://www.submarino.com.br/linha/293729/perfumaria/face",
		"http://www.submarino.com.br/linha/335240/perfumaria/esmaltes",
		"http://www.submarino.com.br/linha/293748/perfumaria/demaquilantes",
		"http://www.submarino.com.br/linha/293591/perfumaria/acessorios",

		"http://www.submarino.com.br/linha/293730/perfumaria/corpo",
		"http://www.submarino.com.br/linha/293788/perfumaria/rosto",
		"http://www.submarino.com.br/linha/293808/perfumaria/cabelos",
		"http://www.submarino.com.br/linha/293592/perfumaria/maos",
		"http://www.submarino.com.br/linha/348148/perfumaria/labios",

		"http://www.submarino.com.br/linha/313742/perfumaria/desodorante",
		"http://www.submarino.com.br/linha/313872/perfumaria/banho",
		"http://www.submarino.com.br/linha/313948/perfumaria/hidratante",
		"http://www.submarino.com.br/linha/313743/perfumaria/pos-barba",
		"http://www.submarino.com.br/linha/349648/perfumaria/protetor-solar",
		"http://www.submarino.com.br/linha/349649/perfumaria/bronzeador-solar",
		"http://www.submarino.com.br/linha/349650/perfumaria/pos-sol",

		"http://www.submarino.com.br/linha/335240/perfumaria/esmaltes",
		"http://www.submarino.com.br/linha/338693/perfumaria/lixas",
		"http://www.submarino.com.br/linha/335293/perfumaria/removedor-de-esmalte",
		"http://www.submarino.com.br/linha/335241/perfumaria/tesouras-e-alicates-de-unha",
		"http://www.submarino.com.br/linha/335273/perfumaria/tratamento-de-unha",
		"http://www.submarino.com.br/linha/335274/perfumaria/tratamento-para-pes",
		"http://www.submarino.com.br/linha/339528/perfumaria/unhas-posticas",
		"http://www.submarino.com.br/linha/339442/perfumaria/adesivo-de-unha"]

    den = re.compile(r'http://www.submarino.com.br((?=.*\/)(?!.*(promocoes.offset|produto)).*)', re.I)
    den_1 = re.compile(r'((?=.*(order|limit|f_)).*)', re.I)

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
        
