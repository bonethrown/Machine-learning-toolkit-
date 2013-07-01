from utils import utils, itemTools
from scrapy import log
from  cosme.pipes.default import AbstractSite
import urllib3
import re
from cosme.settings import HTTP_NUMPOOLS, HTTP_MAXSIZE
import logging
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.pipes.utils.utils import get_http_response, findPrice, strToFloat
import sys
import traceback

logger = logging.getLogger(__name__)

class SephaWeb(AbstractSite):
	
	
	def __init__(self):
		self.http = urllib3.PoolManager(num_pools=HTTP_NUMPOOLS, block=True,maxsize=HTTP_MAXSIZE)
		self.siteModule = XPathRegistry().getXPath('sepha')
			
	def process(self, item, spider, matcher):
		if item['url']:
			item['url'] = item['url'].lower()					
		if item['sku']: 
			item['sku'] = utils.cleanNumberArray(item['sku'],'string')
		if item['price']: 
			item['price'] = itemTools.filterMultiPriceRadio(item)
			item['price'] = utils.cleanNumberArray(item['price'], 'float')
	
		if item['brand']:
			tempBrand = item['brand']
			tempBrand = tempBrand[0]
			tempBrand = utils.extractBrand(tempBrand)
			item['brand'] = tempBrand
		
		if item['name']:
			tempName = item['name']
			tempName = tempName[0]
			item['name'] = utils.cleanChars(tempName)
			#item['volume'] = utils.extractVolume(item['name']) 
		if item['volume']:
			tempName = item['name']
                        tempName = tempName[0]
			item['volume'] = utils.extractVolume(tempName, 'ml')
			
		if item['category']:
			tempCat = item['category']
			item['category'] =utils.cleanChars(tempCat[0])
		if item['image']:
			temp = item['image'] 
			temp = temp[0]
			item['image'] = temp

		if item['product_id']:
			temp = item['product_id']
			try:
				if len(temp) == 1:
					item['comments'] = self.get_comments(temp[0])
			except:
				exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
				logger.error('Error getting comments %s , Exception information: %s, %s, Stack trace: %s ' % (item['url'],
											exceptionType, exceptionValue, traceback.extract_tb(exceptionTraceback)))
				
		return item
	

	def get_comments(self, productId):
		#Eg: 14663
		# TODO: Only the first page is retrieved
		comment_url = 'http://www.sepha.com.br/comentario/produto/id/%s/pagina/1' % (productId)
		rsp = self.http.request('GET', comment_url)
		hxs = get_http_response(rsp.data, comment_url)
		comments = hxs.select(self.siteModule.get_comments()['commentList'])
		result = []
		for comment in comments:
			commentDict = dict()
			commentDict['star'] = self.get_star(comment, 
													self.siteModule.get_comments()['commentStar'])
			if commentDict['star'] is None:
				continue
			commentDict['name'] = comment.select(self.siteModule.get_comments()['commenterName']).extract()
			commentDict['name'] = commentDict['name'][0] if len(commentDict['name']) > 0 else ''
			
			commentDict['date'] = self.get_date(comment, self.siteModule.get_comments()['commentDate'])
			commentText = comment.select(self.siteModule.get_comments()['commentText']).extract()
			commentDict['comment'] = commentText[0].strip() if len(commentText) > 0 else ''
				
			
			result.append(commentDict)
		return result
	
	def get_date(self, comment, pattern):
		datestr  = ''.join(comment.select(pattern).extract()).strip()
		needle= '-'
		idx = datestr.rfind(needle)
		if idx > -1:
			return datestr[idx + len(needle):].strip()
		else:
			return datestr

	def get_star(self, comment, pattern):
		stars = comment.select(pattern)
		return len(stars)
