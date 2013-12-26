from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from cosme.items import CosmeItem
from cosme.spiders.xpaths.xpath_registry import XPathRegistry
from scrapy import log




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
