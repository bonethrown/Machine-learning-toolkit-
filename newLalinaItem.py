
from cosme.dataOps import databaseManager

OUTDB = 'new_collection'
PARENT= ['product_id','price_per_vol','price_str','date_crawled','key','url','site','volume','price','description']
MEMBER= ['date_crawled','product_id']

class Itemgenerator(object):
	def __init__(self, db, coll):
		self.manager = databaseManager(db,coll,coll)
		self.outdb = databaseManager(db,OUTDB)

	def createParent(self, crawl_item):
		item = dict()
		
		for key,value in crawl_item.iteritems():
			print key,value
			if key not in PARENT:
				item[key] = value

			item['sites'] = []
			item['sites'].append(self.addMember(crawl_item))
		return item

	def addMember(self, crawl_item):
		item = dict()
		for key,value in crawl_item.iteritems():
			print key,value
			if key not in MEMBER:
				item[key] = value
		return item

	def firstMember(self, crawl_item):
		item = self.addMember(crawl_item)
		item['parent'] = 1
				
		
