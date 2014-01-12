from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
from scrapy import log

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
		print line
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


	
		


class Gnat(object):

	 def __init__(self, siteModule):
		self.siteModule = siteModule	
		

	 def multiPriceExtract(self, cosmeItem, hxs):
		if len(cosmeItem['price']) == 0: # Check for the 'por' price
			cosmeItem['price'] = hxs.select(self.siteModule.get_price2()).extract()
			print "*******SECOND PRICE CHECK"
			print cosmeItem['price']
		if  len(cosmeItem['price']) == 0:
			cosmeItem['price'] = hxs.select(self.siteModule.get_price3()).extract()
			print "*******************Third price check"
			print cosmeItem['price']
		if  len(cosmeItem['price']) == 0:
			cosmeItem['price'] = hxs.select(self.siteModule.get_price4()).extract()
			print "*******************Fourth price check"
			print cosmeItem['price']
		return cosmeItem['price']

	 def multiVolumeExtract(self, cosmeItem, hxs):
		if  len(cosmeItem['volume']) == 0:
			cosmeItem['volume'] = hxs.select(self.siteModule.get_volume2()).extract()
			print "*******************Second Volume Check"
			print cosmeItem['volume']
			return cosmeItem['volume']
	 def multiNameExtract(self, cosmeItem, hxs):
		if  len(cosmeItem['name']) == 0:
			cosmeItem['name'] = hxs.select(self.siteModule.get_name2()).extract()
			if cosmeItem['name']:
				cosmeItem['name'] = cosmeItem['name'][0]
			print "*******************Second Name Check"
			return cosmeItem['name']