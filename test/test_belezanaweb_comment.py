import unittest

import logging
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.lxmlsel import HtmlXPathSelector
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from test.test_comment_extractor import load_file
from cosme.spiders.Megabot import Cosme

logging.debug('creating logger')
logger = logging.getLogger(__name__)

class TestBelezanaCommentExtract(unittest.TestCase):
    

    xpathRegistry = XPathRegistry()
        
    def test_comment_extraction(self):
        cosme = Cosme()
        sephora_html = load_file('belezanaweb.html')
        #print sephora_html
        url = 'http://www.belezanaweb.com.br/wella-professionals/wella-professionals-enrich-bouncy-foam-mousse-150ml/'
        request = Request(url=url)
        response = HtmlResponse(url=url,
                            request=request,
                            body=sephora_html,
                            encoding = 'utf-8')
        item = self.my_parse_item(response, cosme)
        print '%s ' % item
        
        
    def my_parse_item(self, response, cosme):
        hxs = HtmlXPathSelector(response)
        #cosmeItem['url'] = response.url
        #siteModule = self.xpathRegistry.getXPath(cosmeItem['site'])
        '''
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()
        '''
        siteModule = self.xpathRegistry.getXPath('belezanaweb')        
        return cosme.get_comments(hxs, siteModule)
        