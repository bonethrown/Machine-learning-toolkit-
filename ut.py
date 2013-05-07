#!/usr/bin.python
import unittest
from test.test_comment_extractor import TestCommentExtract
from test.test_laffayette_comment import TestLaffayetteCommentExtract
from test.test_belezanaweb_comment import TestBelezanaCommentExtract
from test.test_magazineluiza_comment import TestMagazineLuizaCommentExtract
from test.test_sepha_comment import TestSephaComment
from test.test_infinitabeleza_comment import TestInfinitaBelezaCommentExtract



def run_test(testcase):
    suite = unittest.TestLoader().loadTestsFromTestCase(testcase)
    unittest.TextTestRunner(verbosity=2).run(suite)    
    
def process():
    #run_test(TestCommentExtract)
    run_test(TestLaffayetteCommentExtract)
    #run_test(TestBelezanaCommentExtract)
    #run_test(TestMagazineLuizaCommentExtract)
    #run_test(TestSephaComment)
    #run_test(TestInfinitaBelezaCommentExtract)
    
if __name__ == '__main__':
    process()
