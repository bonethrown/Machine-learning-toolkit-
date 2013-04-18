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

logger = logging.info(__name__)

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
        
        cosmeItem['comments'] = self.get_comments(hxs, siteModule)
        if COSME_DEBUG:
            raise CloseSpider('Ad-hoc closing for debugging')
        else:
            yield cosmeItem
        
        yield cosmeItem
        
    def get_comments(self, hxs, siteModule):
        comments = hxs.select(siteModule.get_comments()['commentList'])
        result = []
        for comment in comments:
            commentDict = dict()
            commentDict['star'] = self.get_star(comment, 
                                                    siteModule.get_comments()['commentStar'],
                                                    siteModule.get_comments()['commentStar2'])
            if commentDict['star'] is None:
                continue
            commentDict['name'] = comment.select(siteModule.get_comments()['commenterName']).extract()
            if len(commentDict['name']) == 0:
                commentDict['name'] = comment.select(siteModule.get_comments()['commenterName2']).extract()
            commentDict['name'] = commentDict['name'][0] if len(commentDict['name']) > 0 else ''
            commentDict['date'] = self.get_date(comment, siteModule.get_comments()['commentDate'])
            commentText = comment.select(siteModule.get_comments()['commentText']).extract()
            if len(commentText) == 0:
                commentText = comment.select(siteModule.get_comments()['commentText2']).extract()
            commentDict['comment'] = commentText[0].strip()
                
            
            result.append(commentDict)
        return result
    
    def get_date(self, comment, pattern):
        datestr  = ''.join(comment.select(pattern).extract()).strip()
        needle= 'em'
        idx = datestr.find(needle)
        if idx > -1:
            return datestr[idx + len(needle):].strip()
        else:
            return datestr

    def get_star(self, comment, pattern, pattern2):
            possiblestars  = comment.select(pattern).extract()[0]
            # Eg: "width:100%"
            star = 0
            try:
                width = possiblestars.split(':')[1].split('%')[0]
                star = int(float(width)/20)
            except:
                traceback.print_exc(file=sys.stdout)
            return star
