import uuid
from dataOps import databaseManager
import string
from random import getrandbits
OUTDB = 'new_collection'
PARENT= ['_id','product_id','price_per_vol','price_str','date_crawled','url','site','volume','price','description']
MEMBER= ['brand','category','name','name_url','price','site','description','sku','image']
CATEGORY_LIST = ['perfume', 'unha', 'corpo e banho', 'acessorios', 'homem', 'maquiagem', 'cabelo']
class Itemgenerator(object):
	def __init__(self, db, coll):
		self.manager = databaseManager(db,coll,coll)
		#self.manager = databaseManager(db,OUTDB)
	####DEPRECEATED USING EISTING KEY FOR BACKWARD COMPATIBILITTY
	@staticmethod
	def makePrice(price, ref, url):
		#ref is short for reference is the variable the price is tied to, e.g volume in perfumes, color in lipstick, watt in hairdryers
		price = dict()
		price['price'] = price
		price['ref'] = ref
		price['url'] = url
		return price
	
	#there are two cases: 
	#1: items of different volume can have same urls handled in pipeline
	#2: items of different ovlume can have different urls e.g magazineluiza
	# depending on the case the bot needs to fetch all from a single url and update the price arr as a whole or get them 1 by 1 
	def is_url_same(sites_arr):
		check = set(sites_arr)
		if len(check) ==1:
			return True
		else: 
			return False
	
	@staticmethod
	def createParent(crawl_item):
		item = dict()
		
		for key,value in crawl_item.iteritems():
			if key not in PARENT:
				item[key] = value

			item['sites'] = []
			item['sites'].append(Itemgenerator.create_firstMember(crawl_item))
			item['members'] = len(item['sites'])
		return item

	@staticmethod
	def createMember(crawl_item):
		item = dict()
		for key,value in crawl_item.iteritems():
			if key in MEMBER:
				item[key] = value
		return item
	@staticmethod
	def create_firstMember(crawl_item):
		item = Itemgenerator.createMember(crawl_item)
		item['parent'] = 1
		return item
	
	def getParent(self, parent_key):
		coll = self.manager.getCollection()
		item = list(coll.find( { "key" : parent_key }))
		if item:
			out = item[0]
			return out
		else:
			print 'NO Item with that key in db : %s' % coll
				
	def setParent(self, parent, safe = False):	
		if safe:
			if 'key' in parent:
				self.manager.updateLalinaItem(parent)
			else:
				print 'wrong key unable'
		else:
			self.manager.insertItem(parent)
				
	def getMembers(self, parent_key):
		coll = self.manager.getCollection()
		out = list(coll.find( { "key" : parent_key}))
		out = out[0]
		members = out['sites']
		return members

	def get_member(self, parent_key, member):
		mem = self.getMembers(parent_key)
		for item in mem:
			if item['site'] == member:
				return item
			else:
				print 'item site not present in parent'
	def setMember(self, parent_key, member):
		coll = self.manager.getCollection()
		try:
			coll.update( { "key" : parent_key}, { "$push" : { "sites" : member} } )
		except Exception, e: 
			print e

	def removeMember(self, parent_key, member_site):
		coll = self.manager.getCollection()
		coll.update( {"key" : parent_key},  { "$pull" : {"sites" : {"site" : member_site } } })
 
	def removeParent(self, parent_key):	
		coll = self.manager.getCollection()
		coll.remove({ "key" : parent_key})
		print 'removed : %s ' % parent_key
		
	#new format of keeping price and volume in dictionary volume : price , color : price, size : price
	#these are converter methods from original values to and back to crawl items
	#def make_pv_dict(self, pricearr, volumearr):

	#def deconstruct_pv(self, pv_dict):
