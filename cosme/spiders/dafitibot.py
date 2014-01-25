from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.spiders.superSpider import jsPrice
from scrapy import log
#from superSpider import Gnat
from superSpider import PartialCrawler, getJSPrice
import re
 
class Cosme(CrawlSpider):
    

    name = 'Dafbot'
    allowed_domains = ["dafiti.com.br"]
    #might need to change this this is useless for now
    part = PartialCrawler()
    re_allow = part.construct()
    allow_list = [re_allow]

    start = []
    count = 2
    start.append("http://www.dafiti.com.br/beleza-v6-novel-top/") 
    page = 'http://www.dafiti.com.br/beleza-v6-novel-top/?page='
    while (count <24):
	out = page + str(count)
	start.append(out)
	count = count +1
    start_urls = start
   # start_urls = ["http://www.dafiti.com.br/beleza-v6-novel-top/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/cabelos-shampoo/",
#		"http://www.dafiti.com.br/beleza-feminina/cabelos/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/cabelos-condicionador/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/cabelos-finalizador/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/cabelos-mascara/",
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/cabelos-tratamentos-especificos/",
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/cabelos-modelador/",
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/cabelos-acessorios/",
	#	
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/corpo-e-banho/",
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/corpo-e-banho-pos-sol/",
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/corpo-e-banho-banho/",
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/corpo-e-banho-bronzeador/",
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/corpo-e-banho-protetor-solar/",
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/corpo-e-banho-locao-corporal/",
	#	"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/corpo-e-banho-desodorantes/",
	#	
#
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/tratamento/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/tratamento-unhas/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/tratamento-olhos/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/tratamento-corpo/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/tratamento-maos/",
#
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/maquiagem/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/maquiagem-corpo/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/maquiagem-unhas/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/maquiagem-face/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/maquiagem-labios/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/maquiagem-olhos/",
#
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/perfumes/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/kits-e-presentes/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/saude-e-suplemento/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/acessorios/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/acessorios-pincel/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/acessorios-pinca/",
#		"http://www.dafiti.com.br/beleza-feminina-v6-novel-top/beleza-feminina/acessorios-espelho/",
#		]
    #den = r'(http://www.dafiti.com.br/((?!.*(page)).*)$)'
    #den_1 = re.compile(den, re.I)
    deny_list = [r'http://www.dafiti.com.br/((?=.*\/)(?!.*page).*)', r'^((?=.*(sort)).*)$',r'^((?=.*(tamanho)).*)$',r'(http://www.dafiti.com.br/((?=.*(\/)).*)$)']    	
        		
    rules = [
             Rule(SgmlLinkExtractor(allow_domains = allowed_domains, deny= deny_list, allow = allow_list, unique = True), follow=True, callback='parse_item')
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

        cosmeItem['price'] = getJSPrice(hxs.response.body)
	#cosmeItem['price'] = self.gnat.multiPriceExtract(cosmeItem, hxs, self.siteModule)
        #cosmeItem['volume'] = self.gnat.multiVolumeExtract(cosmeItem, hxs, self.siteModule)
        #if not cosmeItem['name']:
         #       cosmeItem['name'] = self.gnat.multiNameExtract(cosmeItem, hxs, self.siteModule)
        #self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
        
