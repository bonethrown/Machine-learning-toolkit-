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
	url = uniqueExt
        priceArray = utils.cleanNumberArray(priceArray, "string")
        print url 
	print priceArray
	print radioArray
	for buttonId in radioArray:
                if buttonId == url:
                        index = radioArray.index(buttonId)
                        price = priceArray[index]
                        return price
		else:
			print "none"
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
		item['price'] = utils.cleanNumberArray(item['price'], 'string')
		#item['price'] = strToFloat(item['price'])
		return item['price']
def hasDiffPrices(item):
	temp = utils.cleanNumberArray(item['price'], 'float') 
	if len(item['price']) > 1 and not utils.isEqualAvg(temp[0], temp):
		return True
	else:
		return False
