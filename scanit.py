from urllib2 import urlopen
import json
from catChecker import Tables
API_KEY = 'KhYatjV0pvcSKFDGuQmaHTJxC_XMSdqO0H8VqibCvT7'
URL = 'https://api.scandit.com/v2/products/'
GOOGLE = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&'


class SkuGen(object):
	def __init__(self):
		self.tableManager = Tables()

	def api_request(self, key):
		api = '?key='+API_KEY
		url = URL + key + api
		response = urlopen(url)
		html = response.read()
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
			
