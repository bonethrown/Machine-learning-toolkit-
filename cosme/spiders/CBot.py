from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import body_or_str, get_base_url, get_meta_refresh
from scrapy.http import Request
from cosme.items import CosmeItem
from scrapy import log
from scrapy.contrib.loader import XPathItemLoader


from xpaths import *
import sys

#TODO Use SitemapSpider instead for magazineluiza.com.br
class Cosme(CrawlSpider):

    name = 'CBot'
    allowed_domains = ['magazineluiza.com.br']   #Add one by one, comment out as necassary
 
    magaRegex = ".?(\/pf\/).?"
    #magaRe = re.compile('.?(\/pf\/pfba\/)$')
    #allowed_domains = ['pornhub.com']
    start_urls = []

    #TODO put these in a file!
    start = ('http://www.magazineluiza.com.br/perfumaria/l/pf/',)
    #start_urls = [start[4]]
    deny_exts = ('games','cams','photos','stories','login\.php','signup\.php','tags\.html','categories\.html','upload.html','search' ,'cat','c=','channel','tag','channels','click','pornstar','community')
    for i in start:
         start_urls.append(i)

    magazine_rule = Rule(SgmlLinkExtractor(allow=(magaRegex),unique=True,deny_extensions=('php'),deny=deny_exts ),callback='parse_item',follow=True)
   
   
    rules = (
	magazine_rule,
		)

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

        x = HtmlXPathSelector(response)
        cosmeItem = CosmeItem()
        
        cosmeItem['site']= self.getDomain(response.url)
        cosmeItem['url'] = response.url
        #Get xpaths that correspond to our domain
        siteModulePath = "cosme.spiders.xpaths."+cosmeItem['site']
        
        #open our xpath for this site
        siteModule = sys.modules[siteModulePath]
        
        #Traverse All our fields in our xpath
        for field in siteModule.META.keys():
            cosmeItem[field] = x.select(siteModule.META[field]).extract()
        
        yield cosmeItem
