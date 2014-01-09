from BeautifulSoup import BeautifulSoup
from utils import utils
import re
from scrapy import log
from scrapy.exceptions import DropItem
import datetime
from  cosme.pipes.default import AbstractSite
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.pipes.utils.utils import get_http_response, cleanNumberArray, multiStateVolume
import sys
import traceback
import logging
import pipeMethods

logger = logging.getLogger(__name__)

class Walmart(AbstractSite):
	
	def __init__(self):
		self.siteModule = XPathRegistry().getXPath('walmart')
		
	def process(self, item, spider, matcher):
		if item['url']:
			item['url'] = item['url'].lower()					
		if item['price']: 
			temp = item['price']
			#pipeline expects price inside list
			arr = []
			arr.append(pipeMethods.combineIntandDec(temp))
			clean = cleanNumberArray(arr, 'float')
			item['price'] = clean
		if item['brand']:
			temp = item['brand']
			item['brand'] = temp[0]

		if item['category']:
			tempCat = item['category']
			item['category'] = tempCat[0]
		
		if item['image']:
			temp = item['image'] 
			temp = temp[0]
			item['image'] = temp
		if item['volume']: 
			temp = item['name']
			item['volume'] = multiStateVolume(temp)
	
		if item['sku']: 
			temp = item['sku']
			temp = temp[0]


		return item
