from utils import utils, itemTools
from scrapy import log
from  default import AbstractSite
import urllib3
import re
from cosme.settings import HTTP_NUMPOOLS, HTTP_MAXSIZE
import logging
from utils.utils import get_http_response, findPrice, strToFloat
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.pipes.utils import stringtools, utils
from cosme.pipes.utils.utils import  extractVolume,stringPrice, strToFloat,extractUrlVolume
import sys
from cosme.pipes.pipeMethods import nonXpathVolume
import traceback
from BeautifulSoup import BeautifulSoup
import urllib
from cosme.pipes.utils.stringtools import isNa
from scrapy.exceptions import DropItem
from cosme.pipes.utils.itemTools import volume2price,hasDiffVolume


logger = logging.getLogger(__name__)

class SephaWeb(AbstractSite):
	
	
	def __init__(self):
		self.http = urllib3.PoolManager(num_pools=HTTP_NUMPOOLS, block=True,maxsize=HTTP_MAXSIZE)
		self.siteModule = XPathRegistry().getXPath('sepha')
			
	def getSephaPrice(self, Arr):
		out = []
		for val in Arr:
			soup = BeautifulSoup(val)
			promoco = soup.findAll('span', {'class': 'precoPromocao'})
			find = soup.findAll('p')
			if promoco:
				promoco = promoco[0]
				pm = promoco.getText()
				pm = stringPrice(pm)
				pm = strToFloat(pm)
				out.append(pm)
			elif find:	
				find = find[0]
				find = find.getText()
				if find:
					pm = stringPrice(find)
					pm = strToFloat(pm)
					out.append(pm)
				else:
					text = soup.getText()
					text = stringPrice(text)
					text = strToFloat(text)
					out.append(text)

		return out

	def process(self, item, spider, matcher):
		if item['url']:
			item['url'] = item['url'].lower()					
		if item['image']:
			http = 'http://'
			if isinstance(item['image'], list):
				temp = item['image'][0]
				temp = temp.replace('//','')
				item['image'] = http+temp
			else:
				temp = item['image']
				temp = temp.replace('//','')
				item['image'] = http+temp
	
		if item['volume']:
			if isinstance(item['volume'], list):
				temp = item['volume']
				temp = utils.getElementVolume(temp)
				item['volume'] = temp

		if item['price']:
				temp = item['price']
				prices = self.getSephaPrice(temp)
				item['price'] = prices
				#if isinstance(item['volume'], list):
				#	price_match, vol = volume2price(item['url'],item['volume'], prices)
				#	item['price'] = price_match
				#	item['volume'] = vol
				#else:	
				#	item['price'] = prices[0]
					
		if item['sku']: 
			item['sku'] = utils.cleanSkuArray(item['sku'],'string')

		if item['brand']:
			temp = item['brand'][0]
                        temp = matcher.dualMatch(temp)
                        item['brand'] = temp
        	if not item['brand']:
                     logging.info(item['url'])
                     raise DropItem("**** **** **** Missing brand in %s . Dropping" % item)			
		if item['category']:
			tempCat = item['category']
			item['category'] =utils.cleanChars(tempCat[0])
	
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
		#rsp = self.http.request('GET', comment_url)
		html = urllib.urlopen(comment_url).read()
        	rsp = html.decode('iso-8859-1')
		hxs = get_http_response(rsp, comment_url)
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
