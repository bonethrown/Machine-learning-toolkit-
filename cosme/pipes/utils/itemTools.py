"""
Module containing some helpful utility functions
"""
import re,datetime,time
from dateutil.parser import parse
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
import logging
import utils
from utils import findPrice, strToFloat
#convert format "13:13" to minutes
logger = logging.getLogger(__name__)
def checkVolume(item):
	if item['volume'] == None:
		item['volume'] = ""
		return item

def keyGen(item):
	key = utils.createKey(item)
	return key

def radioButtonPriceMatch(uniqueExt, priceArray, radioArray):
	url = str(uniqueExt)
        priceArray = utils.cleanNumberArray(priceArray, "string")
	for buttonId in radioArray:
		if re.search(url, buttonId) != None:
                        index = radioArray.index(buttonId)
                        price = priceArray[index]
			return price
	return None                         
def filterMultiPriceRadio(item):
	#temp  = utils.cleanNumberArray(item['price'],'float')
	if hasDiffPrices(item):
		print "*****MULTI PRICE CASE******"
		url = item['url']
		url = re.search(r'\d{2,}', url)
		url = url.group()
		temp = []
		temp.append(radioButtonPriceMatch(url, item['price'], item['sku']))
		#item['price'] = utils.extractPrice(temp)
		#item['price'] = findPrice(temp[0])
		#item['price'] = strToFloat(item['price'])
		return temp
	else:
		temp = []
		temp.append(utils.cleanNumberArray(item['price'], 'string'))
		return temp
def hasMultiPrice(item):
	temp = utils.cleanNumberArray(item['price'], 'float')
	if len(temp) > 1:
		return True
	else:
		return False

def hasDiffPrices(item):
	temp = utils.cleanNumberArray(item['price'], 'float') 
	if len(item['price']) > 1 and not utils.isEqualAvg(temp[0], temp):
		return True
	else:
		return False
