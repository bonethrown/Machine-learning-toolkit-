import unittest

import logging
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from test.test_comment_extractor import load_file

from cosme.pipes.utils import utils
from cosme.pipes.belezanaweb import BelezanaWeb

logging.debug('creating logger')
logger = logging.getLogger(__name__)

class TestBelezanaCommentExtract(unittest.TestCase):
    

    xpathRegistry = XPathRegistry()
        
    def test_comment_extraction(self):
        sephora_html = load_file('belezanaweb.html')
        url = 'http://www.belezanaweb.com.br/wella-professionals/wella-professionals-enrich-bouncy-foam-mousse-150ml/'
        hxs = utils.get_http_response(sephora_html, url)        
        siteModule = self.xpathRegistry.getXPath('belezanaweb')
        
        logger.info('Comments pattern %s ' % (siteModule.META['comments']))
        comment = hxs.select(siteModule.META['comments']).extract()
        self.my_parse_item(comment, siteModule)
        
        
    def test_volume_extraction(self):
        sephora_html = load_file('belezanaweb.html')
        url = 'http://www.belezanaweb.com.br/wella-professionals/wella-professionals-enrich-bouncy-foam-mousse-150ml/'
        hxs = utils.get_http_response(sephora_html, url)        
        siteModule = self.xpathRegistry.getXPath('belezanaweb')
        
        logger.info('name pattern %s ' % (siteModule.META['name']))
        name = hxs.select(siteModule.META['name']).extract()
        
        volume = utils.get_volume(name, 'ml')
        logger.info('%s %s ' % (name , volume))
        
    def my_parse_item(self, comment, siteModule):
        belezanaWeb = BelezanaWeb()
        comments = belezanaWeb.get_comments(comment, 'http://google.com')
        logger.info(comments)
        