from BeautifulSoup import BeautifulSoup
from utils import utils
import re
from scrapy import log
from scrapy.exceptions import DropItem
import datetime
from  cosme.pipes.default import AbstractSite
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.pipes.utils.utils import get_http_response, cleanNumberArray2, multiStateVolume, cleanChars, extractSku,extractFloat
from cosme.pipes.utils.utils2 import allToString
import sys
import traceback
import logging
import pipeMethods
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='branddrop.log', filemode = 'w',level=logging.DEBUG)
class Americanas(AbstractSite):
	
	def __init__(self):
		self.siteModule = XPathRegistry().getXPath('americanas')
		
	def process(self, item, spider, matcher):
		if item['url']:
			item['url'] = item['url'].lower()					
		if item['price']: 
			if item['price'] != 'NA':
				temp = item['price']
				temp = extractFloat(temp)
				#pipeline expects price inside list
				arr = [temp]
				clean = cleanNumberArray2(arr, 'float')
				item['price'] = clean
		if item['name']:
			brand = item['name']
			match = matcher.dualMatch(brand)
			item['brand'] = match
			if not item['brand']:
				logging.info(item['url'])		
				raise DropItem("**** **** **** Missing brand in %s . Dropping" % item)
		
		if item['category']:
			tempCat = item['category']
			item['category'] = tempCat[0]
		
		if item['description']:
			temp = item['description']
                        bad = BeautifulSoup(temp[0])
                        item['description'] = bad.getText()	
	
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
			item['sku'] = extractSku(temp) 

		return item
