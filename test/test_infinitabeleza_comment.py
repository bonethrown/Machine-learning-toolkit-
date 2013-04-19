import unittest

import logging
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from test.test_comment_extractor import load_file
from cosme.pipes.utils import utils
from cosme.pipes.infinitabeleza import InfiniteBeleza

logging.debug('creating logger')
logger = logging.getLogger(__name__)

class TestInfinitaBelezaCommentExtract(unittest.TestCase):
    

    xpathRegistry = XPathRegistry()
        
    def test_comment_extraction(self):
        sephora_html = load_file('infinitabeleza.html')
        url = 'http://www.infinitabeleza.com.br/kit-botox-capilar-loreal-force-vector-cabelos-grossos-pr-2326-238722.htm'
        hxs = utils.get_http_response(sephora_html, url)
        siteModule = self.xpathRegistry.getXPath('infinitabeleza')
        
        logger.info('Comments pattern %s ' % (siteModule.META['comments']))
        comment = hxs.select(siteModule.META['comments']).extract()
        self.my_parse_item(comment, siteModule)
        
        
    def my_parse_item(self, comment, siteModule):
        infiniteBeleza = InfiniteBeleza()
        comments = infiniteBeleza.get_comments(comment, 'http://google.com')
        logger.info(comments)
        
        