from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
#from superSpider import Gnat
from superSpider import PartialCrawler

class Cosme(CrawlSpider):
    

    name = 'Ambot'
    allowed_domains = ["americanas.com.br"]
    #might need to change this this is useless for now
    part = PartialCrawler()
    re_allow = part.construct()


    start_urls = [
		"http://www.americanas.com.br/linha/291275/perfumaria/perfumes",
		"http://www.americanas.com.br/linha/291285/perfumaria/olhos",
		"http://www.americanas.com.br/linha/291488/perfumaria/labios",
		"http://www.americanas.com.br/linha/291508/perfumaria/face",
		"http://www.americanas.com.br/linha/335234/perfumaria/esmaltes",
		"http://www.americanas.com.br/linha/291384/perfumaria/demaquilantes",
		"http://www.americanas.com.br/linha/291535/perfumaria/acessorios",
		"http://www.americanas.com.br/linha/291478/perfumaria/estojos-e-kits",
		"http://www.americanas.com.br/linha/291625/perfumaria/corpo",
		"http://www.americanas.com.br/linha/291848/perfumaria/rosto",
		"http://www.americanas.com.br/linha/291688/beleza-e-saude/tratamentos-de-cabelo",
		"http://www.americanas.com.br/linha/291908/perfumaria/maos",
		"http://www.americanas.com.br/linha/348151/perfumaria/labios",
		"http://www.americanas.com.br/linha/313908/perfumaria/desodorante",
		"http://www.americanas.com.br/linha/313871/perfumaria/banho",
		"http://www.americanas.com.br/linha/313739/perfumaria/locao-corporal",
		"http://www.americanas.com.br/linha/313928/perfumaria/pos-barba",
		"http://www.americanas.com.br/linha/349651/perfumaria/pos-sol",
		"http://www.americanas.com.br/linha/349671/perfumaria/protetor-solar",
		"http://www.americanas.com.br/linha/349672/perfumaria/bronzeador-solar",
		"http://www.americanas.com.br/linha/335234/perfumaria/esmaltes",
		"http://www.americanas.com.br/linha/336492/perfumaria/lixas",
		"http://www.americanas.com.br/linha/335288/perfumaria/removedor-de-esmalte",
		"http://www.americanas.com.br/linha/335236/perfumaria/tesoura-e-alicates-de-unha",
		"http://www.americanas.com.br/linha/335249/perfumaria/tratamento-de-unha",
		"http://www.americanas.com.br/linha/335250/perfumaria/tratamento-para-pes",
		"http://www.americanas.com.br/linha/339440/perfumaria/unhas-posticas",
		"http://www.americanas.com.br/linha/339441/perfumaria/adesivo-de-unha",
		"http://www.americanas.com.br/linha/291563/beleza-e-saude/secadores",
		"http://www.americanas.com.br/linha/291565/beleza-e-saude/shampoo",
		"http://www.americanas.com.br/linha/291558/beleza-e-saude/condicionador",
		"http://www.americanas.com.br/linha/291566/beleza-e-saude/spray-e-gel",
		"http://www.americanas.com.br/linha/291589/beleza-e-saude/chapinhas-pranchas-",]


    #den1 = r'^((?!.*http://www.americanas.com.br/produto).*)$'
    den1 = re.compile(r'http://www.americanas.com.br((?=.*\/)(?!.*(offset|produto)).*)', re.I)
    den2 = re.compile(r'^((?=.*(order|/pop/)).*)$', re.I)
    #den_re = re.compile(r'^((?!.*(produto)).*)$', re.I)
   
    #offset = re.compile(off, re.I)
    deny_list = [den2, den1]
    #den_list = [r'http://www.americanas.com.br((?=.*\/)(?!.*(offset|produto)).*)']    		
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
        hxs = Selector(response)
        cosmeItem = CosmeItem()
        cosmeItem['site'] = self.getDomain(response.url)
        cosmeItem['url'] = response.url
    	siteModule = self.xpathRegistry.getXPath(cosmeItem['site'])
   	#gnat = Gnat(siteModule) 
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.xpath(siteModule.META[field]).extract()

        #cosmeItem['price'] = self.gnat.multiPriceExtract(cosmeItem, hxs, self.siteModule)
        #cosmeItem['volume'] = self.gnat.multiVolumeExtract(cosmeItem, hxs, self.siteModule)
        #if not cosmeItem['name']:
         #       cosmeItem['name'] = self.gnat.multiNameExtract(cosmeItem, hxs, self.siteModule)
        #self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
        
