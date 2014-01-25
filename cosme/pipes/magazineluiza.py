"""
Pipelines per site are stored in their own folder for minumum chaos
"""

from utils import utils
from scrapy import log
import datetime
from cosme.pipes.default import AbstractSite
from cosme.pipes.utils.utils import get_http_response
import sys
import traceback
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
import logging
from BeautifulSoup import BeautifulSoup


logger = logging.getLogger(__name__)

class MagazineLuizaSite(AbstractSite):
    
    def __init__(self):
        self.siteModule = XPathRegistry().getXPath('magazineluiza')

    #Do all default processing here before going on to site specific processing.
    def process(self, item,spider,matcher):

     #   if item['name']:
#	    item['volume'] = utils.extractVolume(item['name'])  
	   
        #if there isn't a price make it very expensive 
        if item['price'] != 'NA':
		item['price'] = utils.cleanNumberArray2(item['price'], 'float')
	
	if item['description']:
		temp = item['description']
		soup = BeautifulSoup(temp[0])
		if soup.section:
			des = soup.section.getText()	
			print des
			item['description'] = des
		else:
			print ' *%%%%%% %%% NO DESCRIPTION' 
			item['description'] = ""
	
        if item['brand']:
            if isinstance(item['brand'], list):
                temp = item['brand']
		temp = utils.cleanChars(temp[0]).lower()
                item['brand'] = temp
            
	if not item['brand']:
		brand = matcher.listMatch(item['name'])
		print 'Lookup match found, %s' % brand
		item['brand'] = brand
	if item['sku']:
		item['sku'] = utils.cleanSkuArray(item['sku'], 'string')			

    # item['brand'] = matcher.listMatch(temp)
        if item['url']:
            item['url'] = item['url'].lower()
        

	if item['category']:
            print "**** CATEGORY ****"
	    if isinstance(item['category'], list):
                temp = item['category']
                item['category'] = temp[0].lower()
            else:
                item['category'] = item['category'].lower()
        if item['comments']:
            comment_html = item['comments']
            try:
                item['comments'] = self.get_comments(comment_html, item['url'])
            except:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                logger.error('Error getting comments %s , Exception information: %s, %s, Stack trace: %s ' % (item['url'],
                                            exceptionType, exceptionValue, traceback.extract_tb(exceptionTraceback)))
                
                
        item['date_crawled'] = utils.convertDateClass(datetime.datetime.today().isoformat())
        return item
             
        
    def get_comments(self, comment_html, url):
        hxs = get_http_response(comment_html[0], url)
        comments = hxs.select(self.siteModule.get_comments()['commentList'])
        result = []
        for comment in comments:
            commentDict = dict()
            commentDict['star'] = self.get_star(comment, 
                                                    self.siteModule.get_comments()['commentStar'],
                                                    self.siteModule.get_comments()['commentStar2'])
            if commentDict['star'] is None:
                continue
            commentDict['name'] = comment.select(self.siteModule.get_comments()['commenterName']).extract()
            if len(commentDict['name']) == 0:
                commentDict['name'] = comment.select(self.siteModule.get_comments()['commenterName2']).extract()
            commentDict['name'] = commentDict['name'][0] if len(commentDict['name']) > 0 else ''
            commentDict['date'] = self.get_date(comment, self.siteModule.get_comments()['commentDate'])
            commentText = comment.select(self.siteModule.get_comments()['commentText']).extract()
            if len(commentText) == 0:
                commentText = comment.select(self.siteModule.get_comments()['commentText2']).extract()
            commentDict['comment'] = commentText[0].strip()
                
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

    def get_star(self, comment, pattern, pattern2):
            possiblestars  = comment.select(pattern).extract()[0]
            # Eg: "width:100%"
            star = 0
            try:
                width = possiblestars.split(':')[1].split('%')[0]
                star = int(float(width)/20)
            except:
                traceback.print_exc(file=sys.stdout)
            return star
        
