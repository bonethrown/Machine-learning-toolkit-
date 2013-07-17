from pymongo import Connection
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz
import hashlib

DB = "testLalina"
NAME_RATIO = 80

def feedtoSolr(batch):
    
    logging.basicConfig(filename= 'feedLog.log', level = logging.DEBUG)

    solr_url = "http://localhost:8080/solr/cosme0/update?json"
    fail = False
    try:
        req  = urllib2.Request(solr_url, data = batch)
        req.add_header("Content-type", "application/json")
        #lets see what we got
        page = urllib2.urlopen(req)
        print "##solr response: %s"%(page)
    except Exception,e :
        logging.debug(e) 
	logging.debug(batch)
	print "problem sending batch %s"%e
        print batch
        fail = True
	
    return fail

#set our batch size
def  createBatch(db,limit=10):
   start = time.time()
   print db.lalina.count()
   hasMatch = False

   for first in  db.testLalina.find():
       	#count = count +1 
	if not hasGroupKey(first):
		for idx,second in enumerate(db.testLalina.find()):
			if objectMatch(first, second):
				second['groupid'] = hashlib.md5(first['key']).hexdigest() 
				outputDb(second)			
				hasMatch = True

			if  idx == db.testLalina.count() and hasMatch:
				print idx
				print 'reached EO scan %s' % db.testLalina.count()	
				first['groupid'] = hashlib.md5(first['key']).hexdigest() 
				outputDb(first)
				hasMatch = False 	
							
					


   end = time.time()
   print "feeding finisehd in %s ms"%(end-start)

def objectMatch(first, second):

	if not hasGroupKey(second):
		if fuzzyMatchBrand(first['brand'], second['brand']):	
			#second['groupid'] = hashlib.md5(first['key']).hexdigest() 
			if matchName(first['name'], second['name']):
				second['groupid'] = hashlib.md5(first['key']).hexdigest() 
				return True
				print 'FULL MATCH'				
			else:
				return False	


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


def lowerandDeascii(name1, name2):
	name1 = name1.lower()
	name2 = name2.lower()
	name1 = fuzz.asciidammit(name1)
	name2 = fuzz.asciidammit(name2)
	return name1, name2 

def matchName(name1, name2):
	name1 = name1.lower()
	name2 = name2.lower()
	name1 = fuzz.asciidammit(name1)
	name2 = fuzz.asciidammit(name2)
	
	ratio = fuzz.token_set_ratio(name1,name2)	
	if ratio > NAME_RATIO:
		print 'name match'
		return True
	else:
		return False
		print 'no match, ratio is %s' % ratio
		
def checkVolume(vol1, vol2):
	if len(vol1) ==0:
		print 'VOL1 has no volume'
		return False
	else:
		if len(vol2) == 0:
			print 'VOL2 has no volume'
			return False
		else:
			print 'both volumes have volume1'
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

def outputDb(item):
        connection = Connection()
        groupDb = connection.comments_db
	try:
		groupDb.outDb.insert(item)
	
	except Exception, e:
		print 'mongo exception'
 

def main(batchSize):
        connection = Connection()
        lalina = connection.comments_db
	createBatch(lalina, limit=batchSize)

if __name__ == "__main__":

    #first argument: batch size
    #second argument: dmp or feed
    #third argument : filename
    main(int(sys.argv[1]))
