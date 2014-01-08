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
import pipeMethods

logger = logging.getLogger(__name__)

class Wallmart(AbstractSite):
	
	def __init__(self):
		self.siteModule = XPathRegistry().getXPath('wallmart')
		
	def process(self, item, spider, matcher):
		if item['url']:
			item['url'] = item['url'].lower()					
		if item['price']: 
			temp = item['price']
			item['price'] = pipeMethods.combineIntandDec(temp)
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
		if item['sku']: 
			temp = item['sku']
			temp = temp[0]


		return item
