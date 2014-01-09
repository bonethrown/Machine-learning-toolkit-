from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
#from superSpider import Gnat

 
class Cosme(CrawlSpider):
    

    name = 'Walbot'
    allowed_domains = ["walmart.com.br"]
    #might need to change this this is useless for now
    cat = re.compile('http://www.walmart.com.br\/categoria/beleza-e-saude\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    
    sec = re.compile('http://www.walmart.com.br\/produto\/Beleza-e-Saude\/secador-de-cabelo\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    mac = re.compile('http://www.walmart.com.br\/produto\/Beleza-e-Saude\/Maquiagem\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    cab = re.compile('http://www.walmart.com.br/produto/Beleza-e-Saude/Shampoo-e-Condicionador\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    cui = re.compile('http://www.walmart.com.br/produto/Beleza-e-Saude/Cuidados-Cabelo\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    tre = re.compile('http://www.walmart.com.br/categoria/beleza-e-saude/tratamento-cabelo\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    esc = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/escova-rotativa\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    cha = re.compile('http://www.walmart.com.br/produto/Beleza-e-Saude/Chapinha\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    esm = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/esmalte\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    cut = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/cutelaria\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    cui = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/cuidado-pele\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    ban = re.compile('http://www.walmart.com.br/produto/Beleza-e-Saude/Cuidado-Banho\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    des = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/desodorante\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    pro = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/protecao-solar\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    cil = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/cilios\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    pin = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/pinceis\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    ace = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/acessorios\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    per = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/perfumes\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    col = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/coloracao\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    mod = re.compile('http://www.walmart.com.br/produto/beleza-e-saude/modelador-de-cabelo\/[\w\-\@?^=%&amp;/~\+#]+', re.I)
    apa = re.compile('http://www.walmart.com.br/categoria/beleza-e-saude/aparador-de-pelo\/[\w\-\@?^=%&amp;/~\+#]+', re.I)

    re_allow = [sec,mac,cab,cui,tre,esc,cha,esm,cut,cui,ban,des,pro,cil,pin,ace,per,col,mod,apa]
	    	
    start_urls = ["http://www.walmart.com.br/departamento/beleza-e-saude/1"]

    deny_exts = [r'http://www.walmart.com.br/categoria/eletronicos\/[\w\-\@?^=%&amp;/~\+#]+', 
		r'http://www.walmart.com.br/categoria/eletrodomesticos\/[\w\-\@?^=%&amp;/~\+#]+',
		r'http://www.walmart.com.br/categoria/bebes\/[\w\-\@?^=%&amp;/~\+#]+',
		r'http://www.walmart.com.br/categoria/informatica\/[\w\-\@?^=%&amp;/~\+#]+',
		r'http://www.walmart.com.br/categoria/telefonia\/[\w\-\@?^=%&amp;/~\+#]+',
		r'http://www.walmart.com.br/categoria/cameras-digitais-e-filmadoras\/[\w\-\@?^=%&amp;/~\+#]+',
		r'http://www.walmart.com.br/departamento\/[\w\-\@?^=%&amp;/~\+#]+']
    		
    rules = [
             Rule(SgmlLinkExtractor(deny = deny_exts, allow_domains = allowed_domains, allow = re_allow, unique = True), follow=True, callback='parse_item')
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
        self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
        
