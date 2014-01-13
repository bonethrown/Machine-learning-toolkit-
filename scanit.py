from urllib2 import urlopen
import json
from cosme.dataOps import databaseManager
from catChecker import Tables
API_KEY = 'KhYatjV0pvcSKFDGuQmaHTJxC_XMSdqO0H8VqibCvT7'
URL = 'https://api.scandit.com/v2/products/'
GOOGLE = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&'


class SkuGen(object):
	def __init__(self):
		self.tableManager = Tables()
		self.outdb = databaseManager('sku','skudatabase')
		self.indb = databaseManager('matching','la1018')

	def api_request(self, key):
		api = '?key='+API_KEY
		url = URL + key + api
		response = urlopen(url)
		html = response.read()
		html = json.loads(html)
		return html

	def googleRequest(self, key):
		callback = 'response_dict'
		context = 'bar'
		query = 'q='+key 
		callback = '&callback=' + callback
		cont = '&context='+context

		url = GOOGLE + query
		response = urlopen(url)
		html = response.read()
		out = json.loads(html)
		out = out['responseData']
			
		return out['results'], getTop(out['results'])

	def getTop(self, arr):
		top = arr[0]
		title = top['title']
		url = top['url']
		return title, url
	
	def api_process(self, api_dict):
		api_dict = api_dict['basic']
		if 'name' in api_dict:
			name = api_dict['name']
			return name
	
	def siteObject(self, item):
		site = dict()
		site['url'] = item['url']
		site['price'] = item['price']
		site['name'] = item['name']
		site['brand'] = item['brand']
		site['category'] = item['category']
		site['description'] = item['description']
		site['image'] = item['image']
		site['price_str'] = item['price_str']
		site['volume'] = item['volume']
		return site
	def newItem(self, sku, name, item):

		new_item = dict()
		new_item['sku'] = sku
		new_item['name'] = name
		new_item['brand'] = item['brand']
		new_item['category'] =item['category']
		new_item['description'] = item['description']
		new_item['sites'] = []
		return new_item		


	def querySku(self, integer):
		collection = self.indb.getCollection()
		for item in collection.find({'site': 'sephora'}).limit(integer):
			sku = item['sku']
			print 'querying sku : %s' % sku
			out = self.api_request(sku)
			print 'response: %s' % out
			name = self.api_process(out)
			print name 
			if name:
				
				new_item = self.newItem(sku,name,item)	
				site = self.siteObject(item)
				site['sku'] = sku
				new_item['sites'].append(site)
				print new_item	
				self.outdb.updateViaSku(new_item)
		




	
