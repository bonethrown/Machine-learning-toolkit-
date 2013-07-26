from utils import utils, itemTools
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
		volume = utils.extractVolume(url)
		if volume != 'NA':
			return volume
		else:
			return 'NA'
