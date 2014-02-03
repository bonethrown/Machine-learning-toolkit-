from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
from cosme.settings import COSME_DEBUG
from scrapy.exceptions import CloseSpider
import logging
import sys
import traceback
from superSpider import PartialCrawler
import re
logger = logging.info(__name__)

#TODO Use SitemapSpider instead for magazineluiza.com.br
class Cosme(CrawlSpider):
    name = 'CBot'
    allowed_domains = ['magazineluiza.com.br']   #Add one by one, comment out as necassary
    part = PartialCrawler()
    re_allow = part.construct()
    print re_allow
    #magaRegex = ".?(\/pf\/).?"
    #magaRe = re.compile('.?(\/pf\/pfba\/)$')
    #allowed_domains = ['pornhub.com']i
    start_urls = ["http://www.magazineluiza.com.br/perfumaria/l/pf/",
	"http://www.magazineluiza.com.br/chapinha/beleza-e-saude/s/cp/chap/",
	"http://www.magazineluiza.com.br/depilador/beleza-e-saude/s/cp/depi/",
	"http://www.magazineluiza.com.br/escovas-e-pentes/beleza-e-saude/s/cp/bsep/",
	"http://www.magazineluiza.com.br/escova-modeladora/beleza-e-saude/s/cp/bsmo/",
	"http://www.magazineluiza.com.br/secador-de-cabelo/beleza-e-saude/s/cp/secc/",
	"http://www.magazineluiza.com.br/shampoo/beleza-e-saude/s/cp/cpsh/",
	"http://www.magazineluiza.com.br/condicionador/beleza-e-saude/s/cp/cpcc/",
	"http://www.magazineluiza.com.br/mascara-e-tratamento-para-o-cabelo/beleza-e-saude/s/cp/cpmt/",
	"http://www.magazineluiza.com.br/modelador-de-cabelo/beleza-e-saude/s/cp/cpmo/",
	"http://www.magazineluiza.com.br/finalizador-para-cabelo/beleza-e-saude/s/cp/cpfi/",
	"http://www.magazineluiza.com.br/estojo-de-maquiagem/beleza-e-saude/s/cp/cpem/",
	"http://www.magazineluiza.com.br/maquiagem-para-os-labios/beleza-e-saude/s/cp/cplb/",
	"http://www.magazineluiza.com.br/maquiagem-para-o-rosto/beleza-e-saude/s/cp/cpro/",
	"http://www.magazineluiza.com.br/maquiagem-para-olhos-e-sobrancelha/beleza-e-saude/s/cp/cpos/",
	"http://www.magazineluiza.com.br/removedor-de-maquiagem/beleza-e-saude/s/cp/cpre/",
	"http://www.magazineluiza.com.br/acessorio-e-maleta-de-maquiagem/beleza-e-saude/s/cp/bsma/",
	"http://www.magazineluiza.com.br/manicure-e-cutelaria/beleza-e-saude/s/cp/bsmc/",
	"http://www.magazineluiza.com.br/esmalte/beleza-e-saude/s/cp/cpes/",
	"http://www.magazineluiza.com.br/produtos-para-uso-no-sol/beleza-e-saude/s/cp/cpso/",
	"http://www.magazineluiza.com.br/perfumes-importados/perfumaria/s/pf/pfpi/",
	"http://www.magazineluiza.com.br/perfume-amadeirado/perfumaria/s/pf/pfam/",
	"http://www.magazineluiza.com.br/perfume-aquatico/perfumaria/s/pf/pfaq/",
	"http://www.magazineluiza.com.br/perfume-citrico/perfumaria/s/pf/pfct/",
	"http://www.magazineluiza.com.br/perfume-especiarado/perfumaria/s/pf/pfep/",
	"http://www.magazineluiza.com.br/perfume-floral/perfumaria/s/pf/pffl/",
	"http://www.magazineluiza.com.br/perfume-frutal/perfumaria/s/pf/pffr/",
	"http://www.magazineluiza.com.br/perfume-oriental/perfumaria/s/pf/pfot/",
	"http://www.magazineluiza.com.br/maquiagem/perfumaria/s/pf/pfma/",
	"http://www.magazineluiza.com.br/batom/perfumaria/s/pf/pfba/",
	"http://www.magazineluiza.com.br/contorno-labial/perfumaria/s/pf/pfcl/",
	"http://www.magazineluiza.com.br/gloss/perfumaria/s/pf/pfgo/",
	"http://www.magazineluiza.com.br/maquiagem-para-o-rosto/perfumaria/s/pf/pfmr/",
	"http://www.magazineluiza.com.br/po-compacto-facial-maquiagem/perfumaria/s/pf/pfcf/",
	"http://www.magazineluiza.com.br/corretivo-p-o-rosto-maquiagem/perfumaria/s/pf/pfcr/",
	"http://www.magazineluiza.com.br/base-maquiagem/perfumaria/s/pf/pfbq/",
	"http://www.magazineluiza.com.br/blush-maquiagem/perfumaria/s/pf/pfbm/",
	"http://www.magazineluiza.com.br/maquiagem-olhos-e-sobrancelhas/perfumaria/s/pf/pfos/",
	"http://www.magazineluiza.com.br/esmaltes-e-acessorios/perfumaria/s/pf/pfea/",
	"http://www.magazineluiza.com.br/esmalte/perfumaria/s/pf/pfes/",
	"http://www.magazineluiza.com.br/bases-removedores-e-acessorios/perfumaria/s/pf/pfra/",
	"http://www.magazineluiza.com.br/cilios-postico-maquiagem/perfumaria/s/pf/pcpo/",
	"http://www.magazineluiza.com.br/acessorios-de-maquiagem/perfumaria/s/pf/pfss/",
	"http://www.magazineluiza.com.br/pincel-de-maquiagem/perfumaria/s/pf/pfim/",
	"http://www.magazineluiza.com.br/maleta-de-maquiagem/perfumaria/s/pf/pfmm/",
	"http://www.magazineluiza.com.br/outros-acessorios-de-maquiagem/perfumaria/s/pf/pfoa/",
	"http://www.magazineluiza.com.br/removedor-de-maquiagem/perfumaria/s/pf/pfre/",
	"http://www.magazineluiza.com.br/condicionador-de-cabelos/perfumaria/s/pf/pfcc/",
	"http://www.magazineluiza.com.br/shampoo/perfumaria/s/pf/pfsh/",
	"http://www.magazineluiza.com.br/finalizador-de-cabelo/perfumaria/s/pf/pfzc/",
	"http://www.magazineluiza.com.br/modelador-de-cabelo/perfumaria/s/pf/pfmd/",
	"http://www.magazineluiza.com.br/tratamento-corporal/perfumaria/s/pf/pftl/",
	"http://www.magazineluiza.com.br/tratamento-para-o-rosto/perfumaria/s/pf/pftr/",
	"http://www.magazineluiza.com.br/tratamento-para-regiao-do-olho/perfumaria/s/pf/pfto/",
	"http://www.magazineluiza.com.br/tratamento-dos-labios/perfumaria/s/pf/pftt/",
	"http://www.magazineluiza.com.br/produtos-p-o-corpo-e-banho/perfumaria/s/pf/pfcb/",
	"http://www.magazineluiza.com.br/tratamento-das-maos/perfumaria/s/pf/pftd/",
	"http://www.magazineluiza.com.br/produtos-para-uso-no-sol/perfumaria/s/pf/pfus/"]

    #TODO put these in a file!
    #start_urls = [start[4]]
    den_1 = re.compile(r'^((?=.*(games|busca|photos|login|php|signup|tags|upload|search|celulares|cama|auto|esportes|tablets)).*)$',re.I)
    deny_list = [den_1]

    magazine_rule = Rule(SgmlLinkExtractor(allow= re_allow,unique=True, deny=deny_list),callback='parse_item',follow=True)
   
   
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
            return segDom[1]
        except:
            return ""
        
    def parse_item(self, response):

        #Lets try using ItemLoaders built into scrapy
        #l = XPathItemLoader(item=CosmeItem(),response=response)

        hxs = HtmlXPathSelector(response)
        cosmeItem = CosmeItem()
        
        cosmeItem['site']= self.getDomain(response.url)
        cosmeItem['url'] = response.url
        #Get xpaths that correspond to our domain
        siteModule = self.xpathRegistry.getXPath(cosmeItem['site'])
                
        #Traverse All our fields in our xpath
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()
        
        yield cosmeItem
        
