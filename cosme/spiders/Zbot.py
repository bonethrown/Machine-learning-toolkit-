from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from cosme.items import CosmeItem
from scrapy import log
from cosme.spiders.xpaths.xpath_registry import XPathRegistry

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
        
class Cosme(CrawlSpider):
    name = 'Zbot'
    allowed_domains = ['sepha.com.br']
    #might need to change this this is useless for now
    start_urls = ["http://www.sepha.com.br",]
    #start = ('http://www.belezanaweb.com.br/perfumes/',)
    
    deny_exts = ('site', 'include', 'ajax', 'basket')
    allow_exts = ('/cat/[\w]+([//\w.]+)')
    #for i in start:
     #   start_urls.append(i)
    #r'/bios/.\w+\.htm'
        #site_rule = RWWule(SgmlLinkExtractor(), follow=True, callback='parse_item')
    rules = [
             Rule(LocalSgmlLinkExtractor(allow = allow_exts, deny = deny_exts) , follow=True, callback='parse_item'),
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
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()
        if len(cosmeItem['price']) == 0: # Check for the 'por' price
            cosmeItem['price'] = hxs.select(siteModule.get_price2()).extract()
        self.log('CosmeItem %s' % cosmeItem,log.INFO)
        yield cosmeItem

