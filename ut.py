#!/usr/bin.python
import unittest
from test.test_comment_extractor import TestCommentExtract
from test.test_laffayette_comment import TestLaffayetteCommentExtract



def run_test(testcase):
    suite = unittest.TestLoader().loadTestsFromTestCase(testcase)
    unittest.TextTestRunner(verbosity=2).run(suite)    
    
def process():
    run_test(TestCommentExtract)

    run_test(TestLaffayetteCommentExtract)
    
if __name__ == '__main__':
    process()
