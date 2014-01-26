from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
#from superSpider import Gnat
from superSpider import PartialCrawler,Gnat
 
class Cosme(CrawlSpider):
    

    name = 'Netbot'
    allowed_domains = ["netfarma.com.br"]
    #might need to change this this is useless for now
    part = PartialCrawler()
    re_allow = part.construct()

    start_urls = ["http://www.netfarma.com.br/categoria.asp?idcategoria=1629&nivel=02&categoria=Maquiagem&topo=s",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2713&nivel=11&categoria=Perfumes&topo=s",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2717&nivel=110102&categoria=Feminino&idP=2713",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2726&nivel=110103&categoria=Unissex&idP=2713",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2718&nivel=110201&categoria=Masculino&idP=2713",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2719&nivel=110202&categoria=Feminino&idP=2713",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2722&nivel=110203&categoria=Unissex&idP=2713",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2741&nivel=110301&categoria=Masculino&idP=2713",
	
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2367&nivel=040108&categoria=Limpeza&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2368&nivel=040109&categoria=Antiacne&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2369&nivel=040110&categoria=Hidratante&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2372&nivel=040113&categoria=Acess%F3rios&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2679&nivel=040205&categoria=Sabonete&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2373&nivel=040203&categoria=Antiss%E9ptico&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2374&nivel=040204&categoria=Hidratante&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2375&nivel=040306&categoria=Sabonete+%CDntimo&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2376&nivel=040307&categoria=Len%E7o+Umedecido&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2378&nivel=040409&categoria=Antitranspirante&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2379&nivel=040410&categoria=Hidratante&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2380&nivel=040411&categoria=%D3leo+Corporal&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2381&nivel=040412&categoria=Sabonete&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2382&nivel=040413&categoria=Acess%F3rios+para+Banho&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2402&nivel=040913&categoria=Condicionador&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2403&nivel=040914&categoria=Creme+de+Pentear&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2404&nivel=040915&categoria=Tratamento&idP=1631",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2669&nivel=020601&categoria=Batom&idP=1629",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2670&nivel=020602&categoria=L%E1pis+para+L%E1bios&idP=1629",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2720&nivel=020603&categoria=Gloss+e+Brilho+Labial&idP=1629",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2671&nivel=020701&categoria=M%E1scara+de+C%EDlios&idP=1629",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2672&nivel=020702&categoria=Sombra&idP=1629",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2673&nivel=020703&categoria=Delineador+de+Olhos&idP=1629",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2689&nivel=020801&categoria=Pinc%E9is&idP=1629",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2723&nivel=020901&categoria=Maletas&idP=1629",
	"http://www.netfarma.com.br/categoria.asp?idcategoria=2724&nivel=020902&categoria=Kit+de+Maquiagem&idP=1629"]
    	
    den_1 = re.compile(r'^((?=.*(fornecedor)).*)$', re.I)

    #deny_list = [den_1]
		
    rules = [
             Rule(SgmlLinkExtractor(allow_domains = allowed_domains, allow = re_allow, unique = True), follow=True, callback='parse_item')
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
        
