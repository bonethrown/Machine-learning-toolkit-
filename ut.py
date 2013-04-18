#!/usr/bin.python
import unittest
from test.test_comment_extractor import TestCommentExtract
from test.test_laffayette_comment import TestLaffayetteCommentExtract
from test.test_belezanaweb_comment import TestBelezanaCommentExtract
from test.test_magazineluiza_comment import TestMagazineLuizaCommentExtract



def run_test(testcase):
    suite = unittest.TestLoader().loadTestsFromTestCase(testcase)
    unittest.TextTestRunner(verbosity=2).run(suite)    
    
def process():
    run_test(TestCommentExtract)
    run_test(TestLaffayetteCommentExtract)
    run_test(TestBelezanaCommentExtract)
    run_test(TestMagazineLuizaCommentExtract)
        
if __name__ == '__main__':
    process()
