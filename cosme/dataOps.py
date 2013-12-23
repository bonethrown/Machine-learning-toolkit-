from pipes.utils import db2, solr, utils
import os, sys
from decimal import *
import pymongo
import urllib
import datetime
#databases
OS_PATH = '/home/dev/pictureStorage/'


DATABASE_MAIN = 'production'
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


class databaseManager(object):

	def __init__(self):
		main_coll = self.databaseNameGen('lalinaraw')
		comment_coll = self.databaseNameGen('comment')
				
		self.connection = db2.getConnection()
		self.hpCollection = db2.getOwnDb(HP, DATABASE_MAIN)
		self.imageCollection = db2.getOwnDb(IMAGE_COL, DATABASE_MAIN)
		self.lalinaCollection = db2.getOwnDb(main_coll, DATABASE_MAIN)
		self.commentsCollection = db2.getOwnDb(comment_coll, DATABASE_MAIN)
		print self.lalinaCollection
		self.remote1Lalina = db2.anyConnection(MIRROR1_DATABASE, main_coll, MIRROR1_HOST, MIRROR1_PORT) 
		self.remote1Comments = db2.anyConnection(MIRROR1_DATABASE, comment_coll, MIRROR1_HOST, MIRROR1_PORT) 
		
	#def updatePrimary(item):
	#### This is the primary function to save an image to the harddrive 
	def databaseNameGen(self, dbtype):
		a = datetime.datetime.utcnow()
		b = a.date().isoformat().replace('-','')
		name = dbtype + '_'+ b
		return name

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
		
	
	def updateComment(self, storeItem):
		if storeItem['comments']:
			try:
				self.commentsCollection.update({"key":storeItem['key']}, {"comments": storeItem['comments'], "url" : storeItem['url'], "key":storeItem['key'], "site": storeItem['site']}, upsert = True)

			except Exception, e:
				log.msg('update error in db for item %s' %item['key']) 

	def updateLalinaItem(self, item):
		try:
			self.lalinaCollection.update({"key" : item['key']}, item, upsert=True)
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


