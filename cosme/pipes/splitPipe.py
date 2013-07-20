"""
Pipelines per site are stored in their own folder for minumum chaos
"""
import copy
from cosme.pipes.default import AbstractSite
from utils import utils, itemTools
from scrapy.exceptions import DropItem
from scrapy import log
import datetime
from cosme.pipes.utils.utils import get_http_response
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
import copy
def keySpace(item):
	item['key'] = ''
	return item

def singularityPipe(item):
	if item['price']:
		temp = item['price']
		item['price'] = []
		temp = temp[0]
		item['price'].append(temp)
	if item['volume']:
		if isinstance(item['volume'], list):
			item['volume'] = item['volume'][0]
	if item['sku']:
		if isinstance(item['sku'], list):
			item['sku'] = item['sku'][0] 
	return item

def isVolumeEqualToPrice(item):
	if len(item['price']) == len(item['volume']):
		return True
	else:
		return False
def addItemVolume(item):
	if isVolumeEqualToPrice:
		out = []
		vol = utils.getElementVolume(item['volume'])
		for v in vol:
			newItem = item
			newItem['volume'] = v
			out.append(newItem)
		return Out

def itemizeByPrice(item):
                responseArray = []
                temp = utils.cleanNumberArray(item['price'], 'float')
                volume = item['volume']
                for price in temp:
                                newItem = copy.deepcopy(item)
                                newItem['price'] = []
                                newItem['volume'] = []
                                newItem['price'].append(price)
                                i = temp.index(price)
                                newItem['volume'] = volume[i]
				print "METRICS GOING IN ***************"
				print volume[i]
				print price
				print newItem
				responseArray.append(newItem)
				del newItem
		return responseArray		
