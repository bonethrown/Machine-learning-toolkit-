"""
Pipelines per site are stored in their own folder for minumum chaos
"""
from cosme.pipes.default import AbstractSite
from utils import utils, itemTools
from scrapy.exceptions import DropItem
from scrapy import log
import datetime
from cosme.pipes.utils.utils import get_http_response
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
import copy

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
		return out

def itemizeByPrice(item):
                responseArray = []
                temp = utils.cleanNumberArray(item['price'], 'float')
                volume = item['volume']
                for price in temp:
                                newItem = copy.copy(item)
                                newItem['price'] = []
                                newItem['volume'] = []
                                newItem['price'].append(price)
                                i = temp.index(price)
                                newItem['volume'] = volume[i]
                                responseArray.append(newItem)
                return responseArray		
