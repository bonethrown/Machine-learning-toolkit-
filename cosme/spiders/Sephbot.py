from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log
import sys
from scrapy.exceptions import CloseSpider
from cosme.settings import COSME_DEBUG


 
class Cosme(CrawlSpider):
    name = 'Sbot'
    allowed_domains = ['sephora.com.br']
    #might need to change this this is useless for now
    
    start_urls = ["http://www.sephora.com.br"]
    #start_urls = ['http://www.sephora.com.br/site/produto.asp?idproduto=13943']
    
    deny_exts = ('include', 'ajax', 'basket', 'orderby')
    allow_exts = (r'site/produto.asp\?idproduto=\d+',r'site/categoria.asp\?idcategoria=\d+', r'site/departamento.asp\?iddepartamento=\d+')
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
        pattern =  siteModule.get_comments()['commentList']        
        comments = hxs.select(pattern)
        result = []
        for comment in comments:
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

