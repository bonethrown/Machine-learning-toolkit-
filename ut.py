#!/usr/bin.python
import unittest
from test.test_comment_extractor import TestCommentExtract

def process():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCommentExtract)
    unittest.TextTestRunner(verbosity=2).run(suite)    
    
if __name__ == '__main__':
    process()
