from BeautifulSoup import BeautifulSoup
from utils import utils
from cosme.pipes.default import AbstractSite
from cosme.pipes.utils.utils import get_http_response
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
import logging
import sys
import traceback

logger = logging.getLogger(__name__)

class InfiniteBeleza(AbstractSite):
    
    def __init__(self):
        self.siteModule = XPathRegistry().getXPath('infinitabeleza')
    
    #do all default processing here
    def process(self, item,spider,matcher):
   	    if item['brand']:
		item['brand'] = item['brand'][0] 
#  	NAME PROVSSED IN DEFAULT PIPLE LINE 
#            if item['name']:
         #       tempNameArr = item['name'][0]
	#	item['name'] = utils.cleanChars(tempNameArr)
            if item['price']:
		  temp = item['price']
		  item['price'] = utils.cleanNumberArray(temp, 'float')

	    if item['volume']:
		item['volume'] = utils.extractVolume(item['name'])
	    if item['comments']:
                comment_html = item['comments']
                try:
                    item['comments'] = self.get_comments(comment_html, item['url'])
                except:
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    logger.error('Error getting comments %s , Exception information: %s, %s, Stack trace: %s ' % (item['url'],
                                            exceptionType, exceptionValue, traceback.extract_tb(exceptionTraceback)))
                
        
            return item
    
    
    def get_comments(self, comment_html, url):
        hxs = get_http_response(comment_html[0], url)
        comments = hxs.select(self.siteModule.get_comments()['commentList'])
        result = []
        for comment in comments:
            commentDict = dict()
            commentDict['star'] = self.get_star(comment, 
                                                    self.siteModule.get_comments()['commentStar'])
            if commentDict['star'] is None:
                continue
            commentDict['name'] = comment.select(self.siteModule.get_comments()['commenterName']).extract()
            commentDict['name'] = utils.cleanChars(commentDict['name'][0] if len(commentDict['name']) > 0 else '')
            
            commentDict['date'] = self.get_date(comment, self.siteModule.get_comments()['commentDate'])
            commentText = comment.select(self.siteModule.get_comments()['commentText']).extract()
            commentDict['comment'] = utils.cleanChars(commentText[0].strip() if len(commentText) > 0 else '')
                
            
            result.append(commentDict)
        return result
    
    def get_date(self, comment, pattern):
        datestr  = ''.join(comment.select(pattern).extract()).strip()
        needle= 'em'
        idx = datestr.find(needle)
        if idx > -1:
            return datestr[idx + len(needle):].strip()
        else:
            return datestr

    def get_star(self, comment, pattern):
        stars = comment.select(pattern)
        star = 0
        spanClasses = stars.extract()
        if len(spanClasses) > 0:
            spanClasses = spanClasses[0]
            for i in range(1, 6):
                thisSpan = 'star%s' % i
                if thisSpan in spanClasses:
                    star = i
                    break
        return star
