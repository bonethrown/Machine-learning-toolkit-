import unittest

import logging
from cosme.spiders.Sephbot import Cosme
import os
from scrapy.http.request import Request
from scrapy.http.response import Response
from cosme.items import CosmeItem
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.lxmlsel import HtmlXPathSelector
from cosme.spiders.xpaths.xpath_registry import XPathRegistry

logging.debug('creating logger')
logger = logging.getLogger(__name__)

class TestCommentExtract(unittest.TestCase):
    

    xpathRegistry = XPathRegistry()
        
    def test_comment_extraction(self):
        cosme = Cosme()
        sephora_html = self.load_file('All is Bright Lip Glaze Set na Sephora.html')
        url = 'http://www.sephora.com.br/site/produto.asp?idproduto=13943'
        request = Request(url=url)
        response = HtmlResponse(url=url,
                            request=request,
                            body=sephora_html,
                            encoding = 'utf-8')
        
        print 'About to parse item'
        item = self.my_parse_item(response, cosme)
        print '%s ' % item
        
    def load_file(self, filename):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        fh = None
        contents = None
        try:
            fh = open(filepath, 'r')
            contents = fh.read()
        except:
            if fh is not None:
                fh.close()
        return contents
        
        
    def my_parse_item(self, response, cosme):
        hxs = HtmlXPathSelector(response)
        #cosmeItem['url'] = response.url
        #siteModule = self.xpathRegistry.getXPath(cosmeItem['site'])
        '''
        for field in siteModule.META.keys():
            cosmeItem[field] = hxs.select(siteModule.META[field]).extract()
        '''
        siteModule = self.xpathRegistry.getXPath('sephora')        
        return cosme.get_comments(hxs, siteModule)
        