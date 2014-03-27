from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.spiders import SitemapSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from cosme.items import CosmeItem
from scrapy import log
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from superSpider import Gnat
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
        
class Cosme(SitemapSpider):
    name = 'Zbotsite'
    #allowed_domains = ['sepha.com.br']
    sitemap_urls = ['http://www.sepha.com.br/sitemap-produto-index.xml']
    
    sitemap_rules = [
        (r'(http://www.sepha.com.br/(?!.*(q=|php|login)).*)', 'parse_item')
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
        gnat = Gnat(siteModule)
	for field in siteModule.META.keys():
            cosmeItem[field] = hxs.xpath(siteModule.META[field]).extract()
	cosmeItem['price'] = gnat.multiPriceExtract(cosmeItem, hxs)	
	cosmeItem['volume'] = gnat.multiVolumeExtract(cosmeItem, hxs)	
	if not cosmeItem['name']:
		cosmeItem['name'] = gnat.multiNameExtract(cosmeItem, hxs, siteModule) 	
	#self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem
 
