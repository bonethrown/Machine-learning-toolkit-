from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.spiders import SitemapSpider, XMLFeedSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from cosme.items import CosmeItem
from scrapy import log
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
import urllib2

sitemap = '/home/dev/kk_cosme/cosme/cosme/spiders/xpaths/aazsitemap.xml'

class LocalSgmlLinkExtractor(SgmlLinkExtractor):
    
    def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(), 
                 tags=('a', 'area'), attrs=('href'), canonicalize=True, unique=True, process_value=None,
                 deny_extensions=None):
        SgmlLinkExtractor.__init__(self, allow=allow, deny=deny, allow_domains=allow_domains, deny_domains=deny_domains,
                                   restrict_xpaths = restrict_xpaths, tags=tags, attrs=attrs, canonicalize=canonicalize,
                                   unique = unique, process_value = process_value, deny_extensions = deny_extensions)
        
    def extract_links(self, response):
        response.body = response.body.replace('<! ', '<!--')
        return SgmlLinkExtractor.extract_links(self, response)
        
class Cosme(XMLFeedSpider):
    name = 'AazBot'
    allowed_domains = ['aazperfumes.com.br']
    start_urls = ['http://www.aazperfumes.com.br/XMLProdutos.asp?IDLoja=434&Any=0&IDProduto=&IDCategoria=&RamoProd=0&PrecoDe=&PrecoAte=&Adicional1=0&Adicional2=0&Adicional3=0&SelImg=0&ExibeDescricao=0&origem=&est=1&DifName=&Mult=&Juros=&UA=False&AddParURL=&Format=0&Brand=0&Size=0']
    sitemap_rules = [(r'^((?=.*(listaprodutos)).*)$', 'parse_item')] 
	
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

    def parse_item(self, response, node):
        hxs = HtmlXPathSelector(response)
        cosmeItem = CosmeItem()
        cosmeItem['site'] = self.getDomain(response.url)
        cosmeItem['url'] = response.url
        siteModule = self.xpathRegistry.getXPath(cosmeItem['site'])
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()
	
	cosmeItem['price'] = self.multiPriceExtract(cosmeItem, hxs, siteModule)
	cosmeItem['volume'] = self.multiVolumeExtract(cosmeItem, hxs, siteModule) 	
	if not cosmeItem['name']:
		cosmeItem['name'] = self.multiNameExtract(cosmeItem, hxs, siteModule) 	
	self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
