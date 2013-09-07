from pipes.utils import db2, solr, utils
import os, sys
from decimal import *
import pymongo
#databases
OS_PATH = '/home/dev/pictureStorage/'

DATABASE_MAIN = 'comments_db'
HP = 'historicalPrices'
IMAGE_COL = 'imagecollection'
COMMENTS_COL = 'itemsTest'
ITEMS_COL = 'lalinaTest'


class databaseManager(object):

	def __init__(self):

		self.connection = db2.getConnection()
		self.connection = self.connection[DATABASE_MAIN]
		self.hpCollection = self.connection[HP]
		self.imageCollection = self.connection[IMAGE_COL]
		self.commentsCollection = self.connection[COMMENTS_COL]
		self.lalinaCollection = self.connection[ITEMS_COL]

	#def updatePrimary(item):
	#### This is the primary function to save an image to the harddrive 

	def updateSecondaryFields(item):
		key = item['key']
		site = item['site']
		picture = item['image']			
		#save the image to filesystem and return path then save path and key to mongodb
		path = self.fileToSave(key, site, picture)
		self.imageSave(key, path)
		self.processPrice(item)	


	def fileToSave(itemKey, itemSite, picture):
		key = itemKey
		site = itemSite
		path = OS_PATH+site+'/'
		if not os.path.exists(path):
			os.makedirs(path)
		completeName = os.path.join(path+"%s.jpg" % key)
		print completeName
		fd = open(completeName, 'w')
		fd.write(picture)
		fd.close()
		return completeName

	def imageSave(key, path):
		imageDict = { 'key': key,
				'path': path}
		
		self.imageCollection.update( { 'key' : key}, imageDict, upsert = True)
 
	
	def priceInsert(key, priceDict, mainDict):
		try:
			self.hpCollection.update( {'key':key}, {'$push': { 'prices' : priceDict} }, mainDict)	
		except Exception, e:
			print 'mongo exception'
			
	def processPrice(item):
		key = item['key']
		date = item['date_crawled']
		out = ''
		groupid = item['groupid'] if ('groupid' in item) else out
		price, hpDict = self.parseHistoricalPrice(date, groupid, item['price'],key , item['volume'], item['name'])
		self.priceInsert(key, price, hpDict)

	
	def parseHistoricalPrice(date, groupid, price, key, volume, name):
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


