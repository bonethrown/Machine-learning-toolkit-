from pipes.utils import db2, solr, utils
import os, sys
from decimal import *
import pymongo
import urllib
import time
#databases
OS_PATH = '/home/dev/pictureStorage/'


DATABASE_MAIN = 'echo'
HP = 'historicalPrices'
IMAGE_COL = 'imagecollection'
COMMENTS_COL = 'itemsTest'
ITEMS_COL = 'lalinaTest'

TEST_LALINA = 'charlie_lalina'
TEST_COMMENT = 'charlie_comment'

MIRROR1_HOST = '23.96.17.252'
MIRROR1_PORT = 27017

MIRROR1_DATABASE = 'mirror1_database'
MIRROR1_LALINA= 'lalina_mirror1'
MIRROR1_COMMENTS = 'commets_mirror1'
TEST_LALINA = 'echo_lalina'
TEST_COMMENT = 'echo_comment'
CATEGORY_LIST = ['perfume', 'unha', 'corpo e banho', 'acessorios', 'homem', 'maquiagem', 'cabelo']


MASTER_HOST = '137.117.83.66'
MASTER_PORT = 27017
MASTER_DATABASE = 'matching'
MASTER_COLL= 'delta'
MASTER_COMMENTS = 'delta_comments'

def nameGen( dbtype):
	a = time.strftime("%B")
	name = dbtype + '_'+ a
	return name

class databaseManager(object):

	def __init__(self, db = DATABASE_MAIN, collection = TEST_LALINA, comment_coll = TEST_COMMENT):
		
		self.db = db2.getConnection(db)
		self.hpCollection = db2.getOwnDb(HP, DATABASE_MAIN)
		self.imageCollection = db2.getOwnDb(IMAGE_COL, DATABASE_MAIN)
		self.lalinaCollection = db2.getOwnDb(collection, db)
		self.commentsCollection = db2.getOwnDb(comment_coll, db)
		self.catdbs = self.initCatCollections()
		self.remote1Lalina = db2.anyConnection(MASTER_HOST, MASTER_PORT,MASTER_DATABASE, MASTER_COLL)
		self.remote1Comments = db2.anyConnection(MASTER_HOST, MASTER_PORT,MASTER_DATABASE, MASTER_COLL)
	
	#def updatePrimary(item):
	#### This is the primary function to save an image to the harddrive 

	def updateRemote(self, item):
		try:
			self.remote1Lalina.update({"key" : item['key']}, item, upsert=True)
		except Exception, e:
			log.msg('update error in db for item %s' %item['key']) 
	
	def updateRemoteComment(self, storeItem):
		if storeItem['comments']:
			try:
				self.remote1Comments.update({"key":storeItem['key']}, {"comments": storeItem['comments'], "url" : storeItem['url'], "key":storeItem['key'], "site": storeItem['site']}, upsert = True)

			except Exception, e:
				log.msg('update error in db for item %s' %item['key']) 
	
	
	def initCatCollections(self):
		dbs =[]
		for cat in CATEGORY_LIST:
			dog  = cat.replace(" ","")
			coll = self.db[dog]
			dbs.append(coll)
		return dbs	
	def databaseNameGen(self, dbtype):
			a = datetime.datetime.utcnow()
			b = a.date().isoformat().replace('-','')
			name = dbtype + '_'+ b
			return name	

	def getCollection(self):
			return self.lalinaCollection
	def getDb(self):
		return self.db
	#def updatePrimary(item):
	#### This is the primary function to save an image to the harddrive 
	def splitByCat(self, cat):
		coll = self.getCollection()
		splitName = cat.replace(" ","")
		splitdb = self.getDb()
		splitdb = splitdb[splitName]

		for item in coll.find({"category": cat}):
			try:
				splitdb.insert(item) 
			except Exception, e:
				print e
	def resetMulti(self, array):
		for db in array:
			self.resetdb(db)
			
	def resetdb(self, collection):
		count = collection.find({ 'matchscore': { "$exists" : True }}).count()
		collection.update( {"groupid" :  { "$exists" : True } }, {"$unset" : { "groupid" : 1 } }, multi = True)	
		collection.update( {"rank" :  { "$exists" : True } }, {"$unset" : { "rank" : 1 } }, multi = True)	
		collection.update( {"matchscore" :  { "$exists" : True } }, {"$unset" : { "matchscore" : 1 } }, multi = True)	
		count_done = collection.find({ 'matchscore': { "$exists" : True }}).count()
		print 'Pre clean Items: %s, post Clean: %s ' % (count, count_done)

	def killdbs(self):
		for db in self.catdbs:
			db.drop()
	
	def chop2cats(self, coll):
		for item in CATEGORY_LIST:
			self.splitByCat(item)
			print 'chopped %s' % item

	def merge(self, parent, slave):
		parent = self.db.create_collection(parent)
		for item in slave.find():
			try:
				parent.insert(item)
			except Exception, e:
				print e

	def multiMerge(self, parent, slaveArr):
		parent = self.db.create_collection('parent')
		for coll in slaveArr:
			for item in coll.find():
				try:
					parent.insert(item)
				except Exception, e:
					print e
	def feedRemote(self, localdb):
		for item in localdb.find():
			self.updateRemote(item)	
				
	def updateComment(self, storeItem):
		if storeItem['comments']:
			try:
				self.commentsCollection.update({"key":storeItem['key']}, {"comments": storeItem['comments'], "url" : storeItem['url'], "key":storeItem['key'], "site": storeItem['site']}, upsert = True)

			except Exception, e:
				log.msg('update error in db for item %s' %item['key']) 
	
	def updateViaSku(self, item):
		try:
			self.lalinaCollection.update({"sku" : item['sku']}, item, upsert=True)
		except Exception, e:
			log.msg('update error in db for item %s' %item['key']) 

	def updateLalinaItem(self, item):
		try:
			self.lalinaCollection.update({"key" : item['key']}, item, upsert=True)
		except Exception, e:
			log.msg('update error in db for item %s' %item['key']) 


	def removeByField(self, field, valueArr):
		num = self.lalinaCollection.find( { field : { '$all': valueArr }}).count()
		print 'Removing : %s' % num 
		try:

			for value in valueArr:
				self.lalinaCollection.remove({field : value})
			done = self.lalinaCollection.find( { field : { '$all': valueArr }}).count()
			print 'Remaining: %s' % done
		except Exception, e:
			log.msg('update error in db for item') 
			
	def updateByField(self, field, value, newValue):
		num = self.lalinaCollection.find({field: value}).count()
		print 'To update : %s' % num 
		try:
			self.lalinaCollection.update({field : value}, {"$set" : {field : newValue}}, multi=True)
			done = self.lalinaCollection.find({field: value}).count()
			print 'Remaining: %s' % done
		except Exception, e:
			log.msg('update error in db for item') 
	
	def updateLalinaField(self, item, field):
		try:
			self.lalinaCollection.update({"key" : item['key']}, {field : item[field]})
		except Exception, e:
			log.msg('update error in db for item %s' %item['key']) 
		
	def updateRemote(self, item):
                try:
                        self.remote1Lalina.update({"key" : item['key']}, item, upsert=True)
                except Exception, e:
                        log.msg('update error in db for item %s' %item['key'])

        def updateRemoteComment(self, storeItem):
                if storeItem['comments']:
                        try:
                                self.remote1Comments.update({"key":storeItem['key']}, {"comments": storeItem['comments'], "url" : storeItem['url'], "key":storeItem['key'], "site": storeItem['site']}, upsert = True)

                        except Exception, e:
                                log.msg('update error in db for item %s' %item['key'])

	def saveImageLocally(self, item):
		picture = self.imageInstance(item['image'])			
		site = item['site']
		key = item['key']
		path = self.fileToSave(key, site, picture)
		self.imageSave(key, path)
	def imageInstance(self, image):
		if isinstance(image, list):
			image = image[0]
			return image
		else:
			return image		
	def updateHistPrice(self, item):
		#save the image to filesystem and return path then save path and key to mongodb
		self.processPrice(item)	

	def fileToSave(self, itemKey, itemSite, picture):
		key = itemKey
		site = itemSite
		path = OS_PATH+site+'/'
		if not os.path.exists(path):
			os.makedirs(path)
		completeName = os.path.join(path+"%s.jpg" % key)
		urllib.urlretrieve(picture, completeName)
		
		print completeName
		#fd = open(completeName, 'w')
		#fd.write(picture)
		#fd.close()
		return completeName

	def imageSave(self, key, path):
		imageDict = { 'key': key,
				'path': path}
		
		self.imageCollection.update( { 'key' : key}, imageDict, upsert = True)
 
	#price insertion and processing methods	
	def priceInsert(self, key, priceDict, mainDict):
		try:
			self.hpCollection.update( {'key': key}, mainDict, upsert = True)
			self.hpCollection.update( {'key':key}, {'$push': { 'prices' : priceDict} })	
		except Exception, e:
			print 'mongo exception'
			
	def processPrice(self, item):
		key = item['key']
		date = item['date_crawled']
		out = ''
		groupid = item['groupid'] if ('groupid' in item) else out
		price, hpDict = self.parseHistoricalPrice(date, groupid, item['price'], key, item['volume'], item['name'])
		self.priceInsert(key, price, hpDict)

	
	def parseHistoricalPrice(self, date, groupid, price, key, volume, name):
		#if unavilable price should be NA 

		priceDict = { 'date': date,
				'price' : price,
				}
		hpDict  = { 'prices' : [],
			    'name' : name,
		    	'key' : key,
			'groupid': groupid,
		    	'volume': volume}
		return priceDict, hpDict


