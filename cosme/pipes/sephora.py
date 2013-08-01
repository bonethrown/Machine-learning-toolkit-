from utils import utils
from cosme.pipes.default import AbstractSite
from cosme.pipes.utils.utils import get_http_response
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.settings import HTTP_MAXSIZE, HTTP_NUMPOOLS
import urllib3
import sys
import traceback
import logging
from cosme.pipes.utils import stringtools
import HTMLParser
from BeautifulSoup import BeautifulSoup
import urllib

logger = logging.getLogger(__name__)

class SephoraSite(AbstractSite):
    
    def __init__(self):
        self.http = urllib3.PoolManager(num_pools=HTTP_NUMPOOLS, block=True,maxsize=HTTP_MAXSIZE)        
        self.siteModule = XPathRegistry().getXPath('sephora')
    
    def process(self, item,spider,matcher):
        if item['url']:
            item['url'] = item['url'].lower()					
        if item['price']: 
		item['price'] = utils.cleanNumberArray(item['price'], 'float')
    
        if item['brand']:
            tempBrand = item['brand']
            tempBrand = tempBrand[0]
            tempBrand = utils.extractBrand(tempBrand)
            item['brand'] = tempBrand
    
       # if item['name']:
        #    tempName = item['name']
         #   tempName = tempName[0]
          #  item['name'] = utils.cleanChars(tempName)
   	if item['volume']:
	 	if not bool(item['volume'][0]):
                        tempName= item['name'][0]
                        item['volume'] = utils.extractVolume(tempName, 'ml')	 
        
	if item['category']:
            tempCat = item['category']
            item['category'] = utils.cleanChars(tempCat[0])
        if item['image']:
            temp = item['image'] 
            temp = temp[0]
            item['image'] = temp
        if item['sku']: 
            item['sku'] = utils.cleanSkuArray(item['sku'], 'string')
        try:
            item['comments'] = self.get_comments(item['url'])
	except:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                logger.error('Error getting comments %s , Exception information: %s, %s, Stack trace: %s ' % (item['url'],
                                            exceptionType, exceptionValue, traceback.extract_tb(exceptionTraceback)))

	#	if item['comments']:
	    
           # item['comments'] = stringtools.decodeIsoComments(item['comments'])
	            
        return item

    def get_comments(self, url):
        comment_url = '%s&view=all' % (url)
        #rsp = self.http.request('GET', comment_url)
        #print rsp.data
	html = urllib.urlopen(comment_url).read()
	rsp = html.decode('iso-8859-1')
	hxs = get_http_response(rsp, comment_url)
        comments = hxs.select(self.siteModule.get_comments()['commentList'])
        result = []
        for comment in comments:
            commentDict = dict()
            commentDict['star'] = self.get_star(comment, self.siteModule.get_comments()['commentStar'])
            commentDict['name'] = comment.select(self.siteModule.get_comments()['commenterName']).extract()[0].strip()
            commentDict['date'] = self.get_date(comment, self.siteModule.get_comments()['commentDate'])
	    commentDict['comment'] = comment.select(self.siteModule.get_comments()['commentText']).extract()[0].strip()
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
            star = 0
            possiblestars  = comment.select(pattern).extract()
            if len(possiblestars) == 1:
                stars = possiblestars[0]
                if 'Avaliacao10' in stars:
                    star = 1
                elif 'Avaliacao20' in stars:
                    star = 2
                elif 'Avaliacao30' in stars:
                    star = 3
                elif 'Avaliacao40' in stars:
                    star = 4
                elif 'Avaliacao50' in stars:
                    star = 5
            return star

