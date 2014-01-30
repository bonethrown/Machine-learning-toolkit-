from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
from scrapy import log
import json
from BeautifulSoup import BeautifulSoup


PERFUME_LIST = '/home/dev/kk_cosme/cosme/cosme/spiders/urllist.list'


class PartialCrawler(object):
	
	def __init__(self):
		self.perfume = self.commaFileToList(PERFUME_LIST)
	
		self.arr = ['perfume','cabelo','unha']
	#	^((?=.*(trunk|tags|branches)).*)$
	
	def test(self, arr):
		string = self.createLinks(arr)	
		out = self._compile(string)
		return out

	def construct(self):
		string = self.createLinks(self.perfume)	
		out = self._compile(string)
		return out

	def createLinks(self, arr):
		line = ''
		for item in arr:
			word = ''+item + '|'
			line = line + word
		line = line[:-1]
		line = '^((?=.*('+ line + ')).*)$'
		return line

	def commaFileToList(self, lookupfile):
                catlist = open(lookupfile)
                masterList = []
                for item in catlist.readlines():
                        item = item.split(',')
                        arr = []
                        for a in item:
                                a = a.decode('utf8')
                                a = a.rstrip()
                                arr.append(a)
                        masterList.extend(arr)
                return masterList

	def _compile(self, string):
		out = re.compile(string, re.I)
		return out


def jsPrice(responseBody):
        soup = BeautifulSoup(responseBody)
        findall = soup.findAll('script')
        return findall
	
def itemTest(findall):
	for item in findall:
    		if re.search(r'dataLayer', str(item)):
         		return item
def getJSPrice(body):
	findall = jsPrice(body)
	item = itemTest(findall)
	text = str(item)
	arr = text.split('\n')
	for element in arr:
		ele =  re.search(r"price", element)
		if ele:
			num = re.search(r'[\d.]+',element)	
			if num:
				num = num.group()
				return num
class Gnat(object):

	 def __init__(self, siteModule):
		self.siteModule = siteModule	

	 def grabAllPrice(self, hxs):
		out = []
		p2 = hxs.select(self.siteModule.get_price2()).extract()
		p3  =hxs.select(self.siteModule.get_price3()).extract()
		p4 = hxs.select(self.siteModule.get_price4()).extract()
		p5 = hxs.select(self.siteModule.get_price5()).extract()
		out.append(p2)
		out.append(p3)
		out.append(p4)
		out.append(p5)
		for items in out:
			if not item:
				out.pop()
					
	 def multiBrandExtract(self, cosmeItem, hxs):
		if not cosmeItem['brand']: # Check for the 'por' price
			cosmeItem['brand'] = hxs.select(self.siteModule.get_brand2()).extract()
		return cosmeItem['brand']
	 def multiPriceExtract(self, cosmeItem, hxs):
		if len(cosmeItem['price']) == 0: # Check for the 'por' price
			cosmeItem['price'] = hxs.select(self.siteModule.get_price2()).extract()
		if  len(cosmeItem['price']) == 0:
			cosmeItem['price'] = hxs.select(self.siteModule.get_price3()).extract()
		if  len(cosmeItem['price']) == 0:
			cosmeItem['price'] = hxs.select(self.siteModule.get_price4()).extract()
		if  len(cosmeItem['price']) == 0:
			cosmeItem['price'] = hxs.select(self.siteModule.get_price5()).extract()
		return cosmeItem['price']

	 def multiVolumeExtract(self, cosmeItem, hxs):
		if not cosmeItem['volume']:
			print 'volcheck 1'
			cosmeItem['volume'] = hxs.select(self.siteModule.get_volume2()).extract()
		if not cosmeItem['volume']:
			print 'volchek 2'
			cosmeItem['volume'] = hxs.select(self.siteModule.get_volume3()).extract()
		return cosmeItem['volume']
	 
	 def multiNameExtract(self, cosmeItem, hxs):
		if  len(cosmeItem['name']) == 0:
			cosmeItem['name'] = hxs.select(self.siteModule.get_name2()).extract()
			if cosmeItem['name']:
				cosmeItem['name'] = cosmeItem['name'][0]
			return cosmeItem['name']
