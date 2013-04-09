from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from cosme.items import CosmeItem

from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
from scrapy.exceptions import CloseSpider
from cosme.settings import COSME_DEBUG

class Cosme(CrawlSpider):
    name = 'Megabot'
    allowed_domains = ['belezanaweb.com.br']
    #might need to change this this is useless for now
    magaRegex = ".?(\/pf\/).?"
    start_urls = ["http://www.belezanaweb.com.br/perfumes/",]
    #start = ('http://www.belezanaweb.com.br/perfumes/',)
    
    deny_exts = ('site', 'include', 'ajax', 'basket')
    allow_exts = (r'[\w\/-]+')
    #for i in start:
    #   start_urls.append(i)
    #r'/bios/.\w+\.htm'
        #site_rule = RWWule(SgmlLinkExtractor(), follow=True, callback='parse_item')
    rules = [
             Rule(SgmlLinkExtractor(allow = allow_exts, deny = deny_exts) , follow=True, callback='parse_item'),
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
        cosmeItem['comments'] = self.get_comments(hxs, siteModule)
        self.log(str(cosmeItem),log.INFO)
        if COSME_DEBUG:
            raise CloseSpider('Ad-hoc closing for debugging')
        else:
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
            possiblestars  = comment.select(pattern).extract()
            if len(possiblestars) == 0:
                possiblestars  = comment.select(pattern2).extract()
            return len(possiblestars)
