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
from cosme.pipes.utils import utils
from cosme.pipes.sephora import SephoraSite

logging.debug('creating logger')
logger = logging.getLogger(__name__)

def load_file(filename):
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

class TestCommentExtract(unittest.TestCase):
    

    xpathRegistry = XPathRegistry()
        
    def test_comment_extraction(self):
        sephora_html = load_file('All is Bright Lip Glaze Set na Sephora.html')
        url = 'http://www.sephora.com.br/site/produto.asp?idproduto=13943'
        hxs = utils.get_http_response(sephora_html, url)
        siteModule = self.xpathRegistry.getXPath('sephora')
        self.my_parse_item(siteModule, url)
        
    def test_volume_extraction(self):
        sephora_html = load_file('All is Bright Lip Glaze Set na Sephora.html')
        url = 'http://www.sephora.com.br/site/produto.asp?idproduto=13943'
        hxs = utils.get_http_response(sephora_html, url)
        siteModule = self.xpathRegistry.getXPath('sephora')
        
        volume = hxs.select(siteModule.META['volume']).extract()
        logger.info(volume)
        
        
    def my_parse_item(self, siteModule, url):
        sephoraSite = SephoraSite()
        comments = sephoraSite.get_comments(url)
        logger.info(comments)
        
        