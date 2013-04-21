import unittest

import logging
from pipes.sepha import SephaWeb



logging.debug('creating logger')
logger = logging.getLogger(__name__)

class TestSephaComment(unittest.TestCase):
    

        
    def test_comment_extraction(self):
        sepha = SephaWeb()
        comments = sepha.get_comments(14663)
        logger.info(comments)
