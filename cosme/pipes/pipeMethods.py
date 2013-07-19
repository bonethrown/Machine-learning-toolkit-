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
from cosme.item import cosmeItem

class GenericPipe(object):
	#THIS IS A GENERIC VOLUME EXTRACTOR THAT WILL CHECK THE NAME THEN URL THEN THE XPATH FOR 
	def __init__(self):
		`

	def GenericPipeVolume(url, name, volume):
	
