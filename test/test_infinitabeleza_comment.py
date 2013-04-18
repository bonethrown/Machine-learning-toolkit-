import unittest

import logging
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.lxmlsel import HtmlXPathSelector
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from test.test_comment_extractor import load_file
from cosme.spiders.CBot import Cosme

logging.debug('creating logger')
logger = logging.getLogger(__name__)

class TestInfinitaBelezaCommentExtract(unittest.TestCase):
    

    xpathRegistry = XPathRegistry()
        
    def test_comment_extraction(self):
        cosme = Cosme()
        sephora_html = load_file('magazineluiza_com.html')
        #print sephora_html
        url = 'http://www.magazineluiza.com.br/ferrari-black-perfume-masculino-eau-de-toilette-75-ml/p/2070190/pf/pffe/'
        request = Request(url=url)
        response = HtmlResponse(url=url,
                            request=request,
                            body=sephora_html,
                            encoding = 'utf-8')
        item = self.my_parse_item(response, cosme)
        print '%s ' % item
        
        
    def my_parse_item(self, response, cosme):
        hxs = HtmlXPathSelector(response)
        siteModule = self.xpathRegistry.getXPath('magazineluiza')        
        return cosme.get_comments(hxs, siteModule)
        