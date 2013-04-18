from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import body_or_str, get_base_url, get_meta_refresh
from scrapy.http import Request
from cosme.items import CosmeItem
from scrapy import log
from scrapy.contrib.loader import XPathItemLoader
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy.exceptions import CloseSpider
from cosme.settings import COSME_DEBUG
from xpaths import *
import sys

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
        self.log('%s gives Price %s of length %s ' % (response.url, cosmeItem['price'], len(cosmeItem['price'])) ,log.INFO)            
        if len(cosmeItem['price']) == 0: # Check for the 'por' price
            self.log('Price: Trying again with regex: %s ' % (siteModule.get_price2()) ,log.INFO)
            cosmeItem['price'] = hxs.select(siteModule.get_price2()).extract()
        cosmeItem['comments'] = self.get_comments(hxs, siteModule)
        self.log('CosmeItem %s' % cosmeItem,log.INFO)
        if COSME_DEBUG:
            raise CloseSpider('Ad-hoc2 closing for debugging')
        else:
            yield cosmeItem

    def get_comments(self, hxs, siteModule):
        pattern =  siteModule.get_comments()['commentList']        
        comments = hxs.select(pattern)
        result = []
        for comment in comments:
            self.log('Processing comments %s ' % comment)
            commentDict = dict()
            commentDict['star'] = self.get_star(comment, siteModule.get_comments()['commentStar'])
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
            self.log('Possible stars %s ' % (possiblestars),log.INFO)
            if len(possiblestars) == 1:
                stars = possiblestars[0]
                if 'Avaliacao10' in stars:
                    star = 1
                elif 'Avaliacao20' in stars:
                    star = 2
                elif 'Avaliacao30' in stars:
                    star = 3
                elif 'Avaliacao40' in stars:
                    star = 4
                elif 'Avaliacao50' in stars:
                    star = 5
            return star

