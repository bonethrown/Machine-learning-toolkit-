from BeautifulSoup import BeautifulSoup
from utils import utils
import re
from scrapy import log
from scrapy.exceptions import DropItem
import datetime
from  cosme.pipes.default import AbstractSite
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.pipes.utils.utils import get_http_response, cleanNumberArray, multiStateVolume, extractSku, cleanChars, cleanHtmlTags
from BeautifulSoup import BeautifulSoup
import sys
import traceback
import logging
import pipeMethods

logger = logging.getLogger(__name__)

class Netfarma(AbstractSite):
	
	def __init__(self):
		self.siteModule = XPathRegistry().getXPath('walmart')
	
	def process(self, item, spider, matcher):
		if item['url']:
			item['url'] = item['url'].lower()					
		if item['price']!= 'NA': 
			temp = item['price']
			clean = cleanNumberArray(temp, 'float')
			item['price'] = clean

		if item['description']:
			item['description'] = item['description'][0]
			soup = BeautifulSoup(item['description'])
			out = soup.getText()
			item['description'] = out		

		if item['name']:
			#temp = item['brand'][0]
			#temp = cleanChars(temp)
			brand = matcher.dualMatch(item['name'])
			item['brand'] = brand
			if not item['brand']:
				raise DropItem("******* Missing BRAND in %s . Dropping" % item['name'])
		#if item['description']:
			#temp = item['description']
			#temp = temp[0]
			#temp = cleanHtmlTags(temp)
			#item['description'] = temp 
		
		if item['category']:
			tempCat = item['category']
			item['category'] = tempCat[0]
			item['category'] = ''	
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
			item['sku'] = ''


		return item
