import unittest

import logging
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from test.test_comment_extractor import load_file
from cosme.pipes.magazineluiza import MagazineLuizaSite
from cosme.pipes.utils import utils

logging.debug('creating logger')
logger = logging.getLogger(__name__)

class TestMagazineLuizaCommentExtract(unittest.TestCase):
    

    xpathRegistry = XPathRegistry()
        
    def test_comment_extraction(self):
        sephora_html = load_file('magazineluiza_com.html')
        url = 'http://www.magazineluiza.com.br/ferrari-black-perfume-masculino-eau-de-toilette-75-ml/p/2070190/pf/pffe/'
        hxs = utils.get_http_response(sephora_html, url)
        siteModule = self.xpathRegistry.getXPath('magazineluiza')
        
        logger.info('Comments pattern %s ' % (siteModule.META['comments']))
        comment = hxs.select(siteModule.META['comments']).extract()
        self.my_parse_item(comment, siteModule, url)
        
        
    def my_parse_item(self, comment, siteModule, url):
        magazineLuiza = MagazineLuizaSite()
        comments = magazineLuiza.get_comments(comment, url)
        logger.info(comments)
        
        