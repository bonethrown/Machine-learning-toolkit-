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

def filterMultiPrice(item):
	temp  = utils.cleanNumberArray(item['price'],'float')

                        if len(item['price']) > 1 and utils.isEqualAvg(temp[0], temp):
                                url = item['url']
                                url = re.search(r'\d+', url)
                                print url
                                temp = utils.radioButtonPriceMatch(url, item['price'], item['sku'])
                                #item['price'] = utils.extractPrice(temp)
                                item['price'] = findPrice(temp[0])
                                item['price'] = strToFloat(item['price'])
                                return item['price']
                        else:
                                item['price'] = utils.extractPrice(item['price'])
                                item['price'] = strToFloat(item['price'])
                                return item['price']
