"""
Module containing some helpful utility functions
"""
import re,datetime,time
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
import logging
import utils
from utils import findPrice, strToFloat
import copy 
from  unidecode import unidecode
from utils import extractVolume,extractUrlVolume
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
			logger.info('price match is: %s type is %s' % (price, type(price)))
			return price

def volume2price(url, volArray,priceArr):
	mark = extractUrlVolume(url)
	index = 0
	for item in volArray:
		if item == mark:
			index = volArray.index(item)
			return priceArr[index], item

def filterMultiPriceRadio(item):
	#temp  = utils.cleanNumberArray(item['price'],'float')
	if hasDiffPrices(item):
		print "*****MULTI PRICE CASE******"
		url = unidecode(item['product_id'][0])
		#url = item['product_id']
		#url = re.search(r'\d{2,}', url)
		#url = url.group()
		temp = []
		#print url 
			
		temp.append(radioButtonPriceMatch(url, item['price'], item['sku']))
		#item['price'] = utils.extractPrice(temp)
		#item['price'] = findPrice(temp[0])
		#item['price'] = strToFloat(item['price'])
		return temp
	else:
		temp  = []
		temp = utils.cleanNumberArray(item['price'], 'string')
		
		logger.info('Diff price false returning only clean string %s price %s' % (temp, type(temp[0])) )
		return temp

def hasDiffVolume(volArray):
	if volArray:
		if len(volArray) > 1 and isinstance(volArray, list):
			temp = volArray
			temp = utils.getElementVolume(temp)
			out = []
			calc = 0
			div = len(volArray)
			if temp:
				for item in temp:
					a = utils.extractFloat(item)
					if a:
						out.append(float(a))
						calc = calc + float(a)
				result = float(calc) / float(div)
				print result
				print out
				if result == out[0]:
					return False
				else:
					return True
		else:
			return False					
			

def hasMultiPrice(item):
	temp = item['price']
	if len(temp) > 1:
		return True
	else:
		return False

def hasDiffPrices(item):
	if isinstance(item['price'][0], str) or isinstance(item['price'][0], unicode):
		temp = copy.deepcopy(item['price'])
		#logger.info('has diff got string instance %s' % temp[0])
		temp = utils.cleanNumberArray(temp, 'float')
	else:
		temp = item['price']

	if len(temp) > 1 and not utils.isEqualAvg(temp[0], temp):
		#logger.info('has diff price outcome: TRUE')
		return True
	else:
		#logger.info('hasdiffprice outcome: FALSE')
		return False
