from pymongo import Connection
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz
import hashlib
import logging

INDB ='lalina'
#secondCon = secondConnection('outDb')
logging.basicConfig(filename='matchLog.log', level=logging.DEBUG)
MAINDB = 'comments_db'
NAME_RATIO = 92

def  matchVolumized(db):
   start = time.time()
   quarter = 0.01
   size =  db.count() -1
   hasMatch = False
   #lookup = db.find()
   print size
   try:
	   for cursor, first in  enumerate(db.find()):
		if not hasGroupKey(first):
			for idx,second in enumerate(db.find()):
				if first['key'] != second['key'] and objectMatch(first,second):
					second['groupid'] = hashlib.md5(first['key']).hexdigest() 
					#outputDb(second,db)
					updateInDb(second,db)			
					hasMatch = True
					print 'FULL MATCH %s' %second['groupid']

				if  idx == size and hasMatch:
					first['groupid'] = hashlib.md5(first['key']).hexdigest() 
					#outputDb(first,db)
					updateInDb(first,db)
					hasMatch = False 	
		print cursor
		if cursor > size*quarter and cursor < (size+30)*quarter:
			quarter = quarter +quarter
			print "percantage done : %s" % quarter						
   except Exception, e:
		print e
		print cursor
		logging.debug(e)		
		logging.debug('Crash occured on cursor count : %s' % cursor)							


   end = time.time()
   print "feeding finisehd in %s ms"%(end-start)

def objectMatch(first, second):

	if not hasGroupKey(second):
		try:
			if fuzzyMatchBrand(first['brand'], second['brand']):
				if matchName(first['name'], second['name']):
					if matchVolume(first['volume'], second['volume']):				
						if first['site'] != second['site']:	
							return True
						else:
							return False	
		except Exception, e:
			logging.debug(e)		
def fuzzyMatchBrand(first, second): 
	first = first.lower()
	first = fuzz.asciidammit(first)
	second = second.lower()
	second = fuzz.asciidammit(second)
	try: 
		ratio = fuzz.ratio(first, second)
	except Exception, e:
		print 'band match error %s' % e
	
	if ratio == 100:
		return True
	else:
		return False

def matchName(name1, name2):
	name1 = name1.lower()
	name2 = name2.lower()
	name1 = fuzz.asciidammit(name1)
	name2 = fuzz.asciidammit(name2)
	
	ratio = fuzz.token_set_ratio(name1,name2)	
	if ratio > NAME_RATIO:
		logging.debug('ratio %s and name %s' % (ratio, name2))
		return True
	else:
		return False
		
def checkVolume(vol1, vol2):
	if vol1 =='NA':
		return False
	else:
		if vol2 == 'NA':
			return False
		else:
			return True

def matchVolume(vol1, vol2):

  if checkVolume(vol1,vol2): 

	ratio = fuzz.ratio(vol1, vol2)
	if ratio == 100:
		return True
		print 'full volume match %s' % ratio
	else:
		return False
		print 'no volume match %s' % ratio
def hasGroupKey(item):
	if 'groupkey' in item:
		return True
	else:
		return False

def secondConnection(secondCollection):
	con = Connection()
	con = con[MAINDB]	
	con = con[secondCollection]
	return con

def outputDb(item, collection):
        
        groupDb = collection

	try:
		groupDb.insert(item)
	
	except Exception, e:
		print 'mongo exception'
 
def updateInDb(item, collection):
        groupDb = collection

	try:
		groupDb.update( {'key': item['key']}, item, safe = True)
	
	except Exception, e:
		print 'mongo exception'

	
def main(collection):
	comments_db = 'comments_db'
        connection = Connection()
	db = connection[comments_db]
	db = db[collection]
	print 'collection in use %s' %db
	matchVolumized(db)

if __name__ == "__main__":

    #first argument: batch size
    #second argument: dmp or feed
    #third argument : filename
    main(str(sys.argv[1]))
