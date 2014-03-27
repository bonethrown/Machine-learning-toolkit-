from utils import utils,utils2, itemTools
from scrapy import log
from  cosme.pipes.default import AbstractSite
import urllib3
import re
from cosme.settings import HTTP_NUMPOOLS, HTTP_MAXSIZE
import logging
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from cosme.pipes.utils.utils import get_http_response, findPrice, strToFloat
import sys
import traceback
from cosme.pipes.utils import utils, itemTools
	#THIS IS A GENERIC VOLUME EXTRACTOR THAT WILL CHECK THE NAME THEN URL THEN THE XPATH FOR 

def sep_url_package(item):
	arr = []
	if isinstance(item['url'], list):
		for url in item['url']:
			pack = package(url)
			arr.append(pack)
	else:
		pack = package(item['url'],item['volume'],item['price'])
		pack = clean_dict(pack)
		arr.append(pack)
			
	return arr

def clean_dict(item):
	out = dict()
	for keys,value in item.iteritems():
		a =utils2.anyToString(value)
		out[keys] = a
	return out

def package(url,vol='',price=''):
	package = dict()
	package['price'] =price
	package['vol'] = vol
	package['url'] = url
	return package

def checkInstance(item):
        if isinstance(item['price'], list) and len(item['price']) > 1:
		if isinstance(item['volume'], list):
			return True
		else: 
			return False
	else:
		return False	

def price_package(item):

	arr = []
	if checkInstance(item):	
		pairs = zip(item['price'], item['volume'])        
		print pairs
		for tup in pairs:
                	package = dict()
			package['price'] = tup[0]
			package['vol'] = tup[1]
			package['url'] = item['url']
			package = clean_dict(package)
			arr.append(package)
	else:

                package = dict()
                package['price'] = item['price']
                package['vol']= item['volume']
                package['url'] = item['url']
		package = clean_dict(package)
                arr.append(package)

        return arr

def brandMatch(stringOrList, matcher):
  if stringOrList:
	if isinstance(stringOrList, list):
		for name in stringOrList:
			brand = matcher.dualMatch(name)
			if brand:
				print 'found match %s' % brand
				return brand
	elif isinstance(stringOrList, str):
		brand = matcher.dualMatch(name)
		if brand:
			print 'found match %s' % brand
			return brand
  else:
	print 'brand is empty'

def genericNameExtract(name):
	if isinstance(name, list):
		name = name[0]
		name = name.lower()
		name = utils.cleanChars(name)
		return name
	else:
		name = name.lower()
		name = utils.cleanChars(name)
		return name

def nonXpathVolume(name, url):
	volume = ''	#this is a generic extractor if the xpath does not have vme 
	name = utils.extractVolume(name)
	if name != 'NA':
		volume = name
		return volume
	else:
		url = url.replace("-"," ").strip()
		volume = utils.extractVolume(url)
		if volume != 'NA':
			return volume
		else:
			return 'NA'

def combineIntandDec(array):
	#wallmart uses this number is integer and decimal
	return array[0]+array[1]

