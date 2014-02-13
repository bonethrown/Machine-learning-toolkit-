from operator import itemgetter
from pymongo import Connection
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz
import hashlib
import logging
from newLalinaItem import Itemgenerator
from copy import copy, deepcopy
from dataOps import databaseManager
from catChecker import Tables
#secondCon = secondConnection('outDb')
logging.basicConfig(filename='matchLog.log', level=logging.DEBUG)
COLLECTION = 'lalina1018'
MAINDB = 'production'
NAME_RATIO = 92
#standard params Name : 90, partial : 61, token : 75
PARTIAL_TOKEN_SORT_RATIO = 61
TOKEN_SORT_RATIO = 75
FULLPROC = False
ADD_TOP_SCORE_DUPLICATE	= True			
IGNORE_VOLUME = True
AVG_THRESH = 83
USE_VOL = False
SWAP_THRESH = 3
MASTER = 'belezanaweb'
MATCH_ORDER = ['sepha','sephora','magazineluiza','laffayette','dafiti','infinitabeleza','americanas','submarino','walmart','netfarma']

class FuzzMatcher(object):

	def __init__(self, db= MAINDB, collection= COLLECTION):
		self.tables = Tables() 
		self.handler = databaseManager(db, collection,collection)
		#self.stopwords = self.filterStopWords('stopwords.list')
		self.memory = []
		self.hasMatch = False
		self.gen = Itemgenerator(db, MASTER)


	## THE FOLLOWING THREE METHODS ARE A NEW MATCHER THEY MATCH BY ORDER WITH THE NEW LALINAITEM OBJECT
	# MASTER : THE PARENT SITE KNOWN AS THE NBENCHMARK COPIED INTO A DATABASE
	#SEQUENTIALLY EACH SITE IS USED TO MATCH AGAINST THE PARENT
	#DESIGINED TO WORK WITH CATEGORY SPLIT DATABSES VIA DATAOPS.SPLITBYCAT
	#RUN WITH CLEANANDCATEGORIZE.PY IN MAPPERSET

	def createMaster(self, db):
                for item in db.find( { 'site' : MASTER }):
                        new_item = self.gen.createParent(item)
                        self.gen.setParent(new_item)

	def getBest(self):
		best = sorted(self.memory, key=itemgetter('score')) 	
		return best[0]

	def siteOrderMatch(self, db):
		master = self.gen.manager.getCollection()
		match_arr = []
		for site in MATCH_ORDER:
			print site
			for cursor, first in master.find(timeout = False):
				size = coll.find( { 'site': site}).count()
				for idx, second in enumerate(db.find( {'site': site} ) ):
					isMatch, score = self.objectMatch_avg(first, second)
					if isMatch:
						second['matchscore'] = score
						self.memory.append(second)
						self.hasMatch = True
					if idx == size and self.hasMatch:
						push = self.getBest(self.memoery)
						push = self.gen.createMember(push)	
						self.gen.setMember(first['key'], push)
						print 'parent: %s  member: %s ' % (first['key'], push)


	def orderLoopMatch(self):
		for db in self.handler.catdbs:
			self.createMaster(db)
			self.siteOrderMatch(db)
		
	def loopMatch(self):

		for db in self.handler.catdbs:
			print 'working Db : %s' % db
			self.dumbMatch(db)
		
	def singleMatch(self):
		self.matchVolumized(self.handler.getCollection())
			
		print 'check test collection %s for results' % collection 
	#def filterStopWords(self,stopFile):
	#	stopList = self.tables.commaFileToList('stopwords.list')	
		#filtered = res = [k for k in lst if 'ab' in k]	
	#	return stopList
	
	def stopfilter(self, name):
		name = name.decode('utf-8')
		name = name.split()
		filtered = [k for k in name if not k in self.stopwords]
		out =" ".join(filtered)
		return out
	def isNotSameKey(self, key1,key2):
		if key1 == key2:
			return False
		else:
			return True

	def dumbMatch(self, db):
		self.memory = []
		start = time.time()
		size =  db.find().count()-1 
		print db
		print 'Item Count: %s' % size
		for cursor, first in  enumerate(db.find(timeout= False)):
			if cursor:
				for idx, second in enumerate(db.find(timeout = False)):
					keycheck = self.isNotSameKey(first['key'], second['key'])
					isMatch, score = self.objectMatch_avg(first, second)
					if keycheck and isMatch:
						second['matchscore'] = score
						if not self.hasExisting(self.memory, second) and not self.hasGroupId(second):
							second['groupid'] = self.stamp(first)
							self.memory.append(second)	
							self.hasMatch = True		
							print 'INSERTING GROUPID:' +  second['groupid'] +' KEY ' + second['key'] 
						else:
							self.replaceHigher(second, first)
					
					if  idx == size and self.hasMatch:
						self.multiUpdate(self.memory, db)
						#self.updateInDb(self.memory[0])
						first['rank'] = '1'
						first['matches'] = len(self.memory) + 1	
						first['groupid'] = hashlib.md5(first['key']).hexdigest() 
						print 'PARENT key: %s ' + first['key']	+ 'parent groupid: ' + first['groupid']			
						self.updateInDb(first, db)
						self.memory = []
						self.hasMatch = False 
		print cursor
		end = time.time()
		print "feeding finisehd in %s ms"%(end-start)
		
							
	#assign score value to object
	def stamp(self,first):
		groupid = hashlib.md5(first['key']).hexdigest()
		return groupid
	def parseSettings(self, settings):
		name_ratio = settings['name_ratio']
		token_ratio = settings['token_ratio']
		partial_ratio = settings['partial_ratio']
		return name_ratio, token_ratio, partial_ratio

	def addScoreDictionary(self, second, first):
		
		name1 = first
		name2 = second
		scoredict = {}
		tokenset = self.fuzzyNameMatch(name1, name2)
		fuzzratio = fuzz.ratio(name1,name2)
		partial_token_sort = fuzz.partial_token_sort_ratio(name1,name2)
		scoredict = { 'tokenset' : tokenset,
				'fuzzratio': fuzzratio,
				'partialsort' : partial_token_sort }
		return scoredict
	def stampScore(self,first, second):
		score = self.fuzzyNameMatch(first['name'], second['name'])	
		return score	
	#check to replace a betterMatch

		
	def replaceHigher(self, toAdd, first):
		if self.hasExisting(self.memory, toAdd):
			for item in self.memory:
				if item['site'] == toAdd['site']:
					if self.checkScore(item['matchscore'], toAdd['matchscore']):
							self.memory = [d for d in self.memory if d.get('site') != toAdd['site']]
							toAdd['groupid'] = self.stamp(first)
							self.memory.append(toAdd)
							print 'Adding score: %s removing : %s ' %(toAdd['matchscore'], item['matchscore'])


	def compareOverallScores(self, item1, itemNew):
		score1 = item1['matchscore']
		score2 = itemNew['matchscore']
		tokenset = (score1['tokenset'], score2['tokenset'])
		partialsort = (score1['partialsort'],score2['partialsort'])
		fuzzratio = (score1['fuzzratio'], score2['fuzzratio'])
		
		setBool = self.checkTupScore(tokenset)	
		partialBool = self.checkTupScore(partialsort)
		fuzzBool = self.checkTupScore(fuzzratio)
		if setBool and partialBool:
			return True
		elif setBool and fuzzBool:
			return True
		elif fuzzBool and partialBool:
			return True

		else: 
			return False
	
	def hasExisting(self,memory, toAdd):
		hasItem = bool
		if len(memory) > 0:
			for item in memory:
				if item['site'] == toAdd['site']:
					return True
				else:
					hasItem = False
			return hasItem
		else:
			return False
	def checkTupScore(self, tupple):
		score1 = tupple[0]
		score2 = tupple[1]	
		if score1 < score2:
			return True
		elif score1 > score2:
			return False
		elif score1 == score2:
			return True				

	def checkScore(self,score1, score2):
		score1 = score1 + SWAP_THRESH	
		if score1  < score2:
			return True
		elif score1 > score2:
			return False
		elif score1 == score2:
			return False				

	def objectMatch_avg(self, first, second):
		if first['site'] != second['site']:
			if self.fuzzyMatchBrand(first['brand'], second['brand']):
				if USE_VOL:
					vol_match = self.matchVolume(first['volume'], second['volume'])
					if vol_match:
						hasMatch, score = self.avgScoreMatch(first['name'],second['name'])
						return hasMatch, score	
					else:
						return False, 0 	
				else:
					hasMatch, score = self.avgScoreMatch(first['name'],second['name'])
					return hasMatch, score	
			else:
				return False, 0	
		else:
			return False, 0
									

	def fuzzyMatchBrand(self, first, second): 
		first = first.lower().strip()
		#first = fuzz.asciidammit(first)
		second = second.lower().strip()
		#second = fuzz.asciidammit(second)
		ratio = fuzz.ratio(first, second)
		if ratio >= 98:
			return True
		else:
			return False
	def avgScoreMatch(self, name1, name2):
		score  = self.triFuzzyMatch(name1,name2)
		name = score['nameratio']
		part = score['partial']
		token = score['token']

		total =  float(name) + float(part) + float(token)
		avg = float(total) / 3
		#print 'avg score : %s total score : %s ' % (avg, total)
		if avg >= AVG_THRESH:
			return True, avg
		else:
			return False, avg


	def triFuzzyMatch(self, name1, name2):
		score1 = self.fuzzyNameMatch(name1,name2)
		score2 = self.partialTokenMatch(name1,name2)
		score3 = self.tokenSortMatch(name1,name2)	
		scores = dict()
		scores = { 'nameratio'	: score1,
				'partial' : score2,
				'token' : score3}
		#for key, value in scores.iteritems():
		#	if value == False:
		#		return False
		#	else:
		return scores

	def fuzzyNameMatch(self, name1, name2):
		ratio = fuzz.token_set_ratio(name1,name2)	
		return ratio 

	def partialTokenMatch(self, name1,name2):
		ratio = fuzz.partial_token_sort_ratio(name1,name2)
		return ratio
	def partialTokenCheck(self, name1, name2):
		ratio = self.partialTokenMatch(name1,name2)
		if ratio > PARTIAL_TOKEN_SORT_RATIO:
			return True, ratio
		elif ratio < PARTIAL_TOKEN_SORT_RATIO:
			return False, ratio
		elif ratio == PARTIAL_TOKEN_SORT_RATIO:
			return True, ratio
	
	def tokenSortMatch(self, name1, name2):
		ratio = fuzz.token_sort_ratio(name1,name2)
		return ratio
	def tokenCheck(self, name1, name2):
		ratio = self.tokenSortMatch(name1,name2)
		if ratio > TOKEN_SORT_RATIO:
			return True, ratio
		elif ratio < TOKEN_SORT_RATIO:
			return False, ratio
		elif ratio == TOKEN_SORT_RATIO:
			return False, ratio

	def matchName(self, name1, name2):
		ratio = fuzz.token_set_ratio(name1,name2)	
		if ratio > NAME_RATIO:
			return True, ratio
		else:
			return False, ratio
			
	def checkVolume(self, vol1, vol2):
		if vol1 =='NA':
			return False
		else:
			if vol2 == 'NA':
				return False
			else:
				return True

	def matchVolume(self, vol1, vol2):

		if vol1 == 'na' or vol2 == 'na':
			return True
		ratio = fuzz.ratio(vol1, vol2)
		if ratio == 100:
			return True
		else:
			return False

	def hasGroupId(self, item):
		if 'groupid' in item:
			return True
		else:
			return False
	 
	def synthMulti(self, array):
		for item in array:
			try:	
				self.updateInDb(item) 
			except Exception, e:
				print ' Exception %s ' % e
	
	def updateInDb(self, item, db):
		
		db.update( {'key': item['key']}, item, safe = True)
		
	def multiUpdate(self, array, db): 
		try:
			for item in array:
				db.update( {'key' :item['key']} , item, safe = True)  
		except Exception, e:
			print "MONGO ERROR %s " % e
		
def main(collection):
	a = fuzzMatcher()
	a.matchVolumized()
if __name__ == "__main__":

    #first argument: batch size
    #second argument: dmp or feed
    #third argument : filename
    main(str(sys.argv[1]))
