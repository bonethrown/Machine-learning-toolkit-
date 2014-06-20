from cosme.pipes.belezanaweb import BelezanaWeb
from cosme.pipes.sephora import SephoraSite
from cosme.pipes.magazineluiza import MagazineLuizaSite
from cosme.pipes.infinitabeleza import InfiniteBeleza
from cosme.pipes.default import AbstractSite
from cosme.pipes.sepha import SephaWeb
from cosme.pipes.laffayette import laffayetteWeb
from cosme.pipes.americana import Americanas
from cosme.pipes.submarino import Submarino
from cosme.pipes.walmart import Walmart
from cosme.pipes.dafiti import Dafiti
from cosme.pipes.netfarma import Netfarma
import json, urllib2
from cosme.pipes import pipeMethods
from  pipes.utils import db,utils, itemTools, db2
from cosme import dataOps
from cosme.dataOps import nameGen
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.crawler import Crawler

SETTINGS = 'settings.py'
TEST = {'key': u'1b7a4cdb5aedc8d23d4a47cff63b241c',
  'sites': [{u'price': u'331.9',
    'site': u'belezanaweb',
    u'url': u'http://www.belezanaweb.com.br/bvlgari/omnia-coral-feminino-eau-de-toilette/',
    u'vol': u'40ml'},
   {u'price': u'468.9',
    'site': u'belezanaweb',
    u'url': u'http://www.belezanaweb.com.br/bvlgari/omnia-coral-feminino-eau-de-toilette/',
    u'vol': u'65ml'}]}

class Controller(object):
	def __init__(self):
		self.settings = SETTINGS
		self.crawler = Crawler(self.settings)
		self.table = [TEST]

	def is_url_same(self, arr):
		check = []
		for item in arr:
			check.append(item['url'])
			s = set(check)
		if len(s) > 1:
			return False
		else:
			return True	


class Hoss_pipeline(object):
	def __init__(self):
		self.pipes = Pipe_Manager()		

class Url_list(object):
	def __init__(self):
		self.dbManager = dataOps.databaseManager('sites3','merged', 'merger')
		self.arr = self.process_url() 

	def process_url(self):
		coll = self.dbManager.getCollection()
		arr = []
		for item in coll.find():
			crawl_dic = self.parse(item)	
			arr.append(crawl_dic)
		return arr

			
	def parse(self, item):
		crawl_dic = dict()
		crawl_dic['key'] = item['key']
		crawl_dic['sites'] = []	
		
		for site_item in item['sites']:
			site = site_item['site']
			price_arr = site_item['price']
			
			for item in price_arr:
				item['site'] = site
		
			crawl_dic['sites'].extend(price_arr)		

		#crawl_dic['sites'] = price_arr		
		return crawl_dic

class Pipe_Manager(object):
	def __init__(self):

		self.siteDict = dict()
		self.siteDict['belezanaweb'] = BelezanaWeb()
		self.siteDict['sephora'] = SephoraSite()
		self.siteDict['magazineluiza'] = MagazineLuizaSite()
		self.siteDict['infinitabeleza'] = InfiniteBeleza()
		self.siteDict['default'] = AbstractSite()
		self.siteDict['sepha'] = SephaWeb()
		self.siteDict['laffayette'] = laffayetteWeb()
		self.siteDict['walmart'] = Walmart()
		self.siteDict['submarino'] = Submarino()
		self.siteDict['americanas'] = Americanas()
		self.siteDict['dafiti'] = Dafiti()
		self.siteDict['netfarma'] = Netfarma()
		self.defaultSite = AbstractSite()



