from pipeMethods import price_package
from BeautifulSoup import BeautifulSoup
from utils import utils
import re
from scrapy import log
from scrapy.exceptions import DropItem
import datetime
from  cosme.pipes.default import AbstractSite
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.pipes.utils.utils import get_http_response
import sys
import traceback
import logging
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)

class laffayetteWeb(AbstractSite):
	
	def __init__(self):
		self.siteModule = XPathRegistry().getXPath('laffayette')
		
	def process(self, item, spider, matcher):
		if item['url']:
			item['url'] = item['url'].lower()					
		if item['price'] != 'NA': 
			item['price'] = utils.cleanNumberArray(item['price'], 'float')
	
		if item['brand']:
			temp = item['brand'][0]
			temp = matcher.dualMatch(temp)
			item['brand'] = temp
		if not item['brand']:
			     logging.info(item['url'])
			     raise DropItem("**** **** **** Missing brand in %s . Dropping" % item)	
		
		if item['description']:
                	
			temp = item['description']
			bad = BeautifulSoup(temp[0])
			item['description'] = bad.getText()
		
		if item['volume']:
			#volume can be string or list depening on item count on particular page
			temp = item['volume']
			if isinstance(temp, list):
				if len(temp) > 1:
					temp = utils.getElementVolume(temp)
					item['volume'] = temp
			else:
				item['volume'] = utils.extractVolume(item['volume'])

		if item['category']:
			tempCat = item['category']
			item['category'] =utils.cleanChars(tempCat[0])
		if item['image']:
			temp = item['image'] 
			temp = temp[0]
			item['image'] = temp
		if item['sku']: 
			temp = item['sku']
			temp = temp[0]

		if item['comments']:
			comment_html = item['comments']
			try:
				item['comments'] = self.get_comments(comment_html, item['url'])
			except:
				exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
				logger.error('Error getting comments %s , Exception information: %s, %s, Stack trace: %s ' % (item['url'],
											exceptionType, exceptionValue, traceback.extract_tb(exceptionTraceback)))
				

		temp = price_package(item)
        	item['price'] = temp
		print ' big pacakge: %s' % temp	
		return item


	def get_comments(self, comment_html, url):
		hxs = get_http_response(comment_html[0], url)
		comments = hxs.select(self.siteModule.get_comments()['commentList'])
		result = []
		for comment in comments:
			commentDict = dict()
			commentDict['star'] = self.get_star(comment, self.siteModule.get_comments()['commentStar'])
			if commentDict['star'] is None:
				continue
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
				if 'level1' == stars:
					star = 1
				elif 'level2' == stars:
					star = 2
				elif 'level3' == stars:
					star = 3
				elif 'level4' == stars:
					star = 4
				elif 'level5' == stars:
					star = 5
			else:
				star = None
			return star
