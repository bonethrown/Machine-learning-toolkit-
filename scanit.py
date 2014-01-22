from urllib2 import urlopen
from urllib3 import HTTPConnectionPool, PoolManager
from urllib3.util import Timeout
import json
from cosme.pipes.utils import utils
from cosme.dataOps import databaseManager
from catChecker import Tables
API_KEY = 'KhYatjV0pvcSKFDGuQmaHTJxC_XMSdqO0H8VqibCvT7'
URL = 'https://api.scandit.com/v2/products/'
GOOGLE = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
REQUEST_AMOUNT = 10

class SkuGen(object):
	def __init__(self):
		self.tableManager = Tables()
		self.outdb = databaseManager('sku','skudatabase')
		self.indb = databaseManager('matching','la1018')
		self.pool = PoolManager(REQUEST_AMOUNT)
		self.request = self.pool.connection_from_url(URL)

	def api_request(self, key):
		api = '?key='+API_KEY
		url = URL + key + api
		data = self.request.urlopen('GET', url)
		value = data.data
		data.close()
		print value
		try:
			out = json.loads(value)
			return out
		except Exception:
			pass

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
		new_item['sites'] = []
		return new_item		


	def querySku(self, integer, site):
		collection = self.indb.getCollection()
		count = 0
		for item in collection.find({'site': site}).limit(integer):
			sku = item['sku']
			_sku = str(utils.extractSku(sku))
			print 'querying sku : %s' % sku
			out = self.api_request(_sku)
			try:
				name = self.api_process(out)
				print name 
				count = count + 1
				print count
				if name:
					
					new_item = self.newItem(sku,name,item)	
					site = self.siteObject(item)
					site['sku'] = sku
					new_item['sites'].append(site)
					self.outdb.updateViaSku(new_item)
			
			except Exception:
				pass		




	
