from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from cosme.items import CosmeItem
from scrapy import log
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.settings import COSME_DEBUG
from scrapy.exceptions import CloseSpider

class Cosme(CrawlSpider):
    name = 'Lafbot'
    allowed_domains = ['laffayette.com.br']
    #might need to change this this is useless for now
    magaRegex = ".?(\/pf\/).?"
    start_urls = ["http://www.laffayette.com.br/",]
    #start = ('http://www.belezanaweb.com.br/perfumes/',)
    
    deny_exts = ('site', 'include', 'ajax', 'basket')
    allow_exts = ('fill in stuff')
    #for i in start:
    #   start_urls.append(i)
    #r'/bios/.\w+\.htm'
        #site_rule = RWWule(SgmlLinkExtractor(), follow=True, callback='parse_item')
    rules = [
             Rule(SgmlLinkExtractor(allow = ('produto'), deny = deny_exts) , follow=True, callback='parse_item'),
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
            commentDict['star'] = self.get_star(comment, siteModule.get_comments()['commentStar'])
            if commentDict['star'] is None:
                continue
            commentDict['name'] = comment.select(siteModule.get_comments()['commenterName']).extract()[0].strip()
            commentDict['date'] = self.get_date(comment, siteModule.get_comments()['commentDate'])
            commentDict['comment'] = comment.select(siteModule.get_comments()['commentText']).extract()[0].strip()
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

    def get_star(self, comment, pattern):
            star = 0
            possiblestars  = comment.select(pattern).extract()
            if len(possiblestars) == 1:
                stars = possiblestars[0]
                if 'level1' == stars:
                    star = 1
                elif 'level2' == stars:
                    star = 2
                elif 'level3' == stars:
                    star = 3
                elif 'level4' == stars:
                    star = 4
                elif 'level5' == stars:
                    star = 5
            else:
                star = None
            return star