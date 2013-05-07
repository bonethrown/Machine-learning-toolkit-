import unittest

import logging
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from test.test_comment_extractor import load_file
from cosme.pipes.utils import utils
from cosme.pipes.laffayette import laffayetteWeb

logging.debug('creating logger')
logger = logging.getLogger(__name__)

class TestLaffayetteCommentExtract(unittest.TestCase):
    

    xpathRegistry = XPathRegistry()
        
    def test_comment_extraction(self):
        sephora_html = load_file('Laffayette.html')
        url = 'http://www.laffayette.com.br/produto/esmalte-revlon-scented-nail-enamel-14,7ml.html'
        hxs = utils.get_http_response(sephora_html, url)
        siteModule = self.xpathRegistry.getXPath('laffayette')
        
        logger.info('Comments pattern %s ' % (siteModule.META['comments']))
        comment = hxs.select(siteModule.META['comments']).extract()
        self.my_parse_item(comment, siteModule)
        

    def test_volume_extraction(self):
        sephora_html = load_file('Laffayette.html')
        url = 'http://www.laffayette.com.br/produto/esmalte-revlon-scented-nail-enamel-14,7ml.html'
        hxs = utils.get_http_response(sephora_html, url)
        siteModule = self.xpathRegistry.getXPath('laffayette')
        
        logger.info('name pattern %s ' % (siteModule.META['name']))
        name = hxs.select(siteModule.META['name']).extract()
        
        lweb = laffayetteWeb()
        volume = lweb.get_volume(name)
        logger.info('%s %s ' % (name , volume))

        
    def my_parse_item(self, comment, siteModule):
        laffayetteSite = laffayetteWeb()
        comments = laffayetteSite.get_comments(comment, 'http://google.com')
        logger.info(comments)
        