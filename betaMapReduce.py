from pymongo import Connection
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz
import hashlib
import logging
from copy import copy, deepcopy
#secondCon = secondConnection('outDb')
logging.basicConfig(filename='matchLog.log', level=logging.DEBUG)
COLLECTION = 'mapvseven'
MAINDB = 'matching'
NAME_RATIO = 92
PARTIAL_TOKEN_SORT_RATIO = 61
TOKEN_SORT_RATIO = 75
FULLPROC = False
ADD_TOP_SCORE_DUPLICATE	= True			


class fuzzMatcher(object):

	def __init__(self):
		self.memory = []
		connection = Connection()
		db = connection[MAINDB]
		db = db[COLLECTION]
		self.db = db
		self.hasMatch = False

	def singleMatch(self):
		comments_db = 'matching'
		collection = 'unittest'
		connection = Connection()
		db = connection[comments_db]
		self.db = db[collection]
		self.matchVolumized()
			
		print 'check test collection %s for results' % collection 

	def  matchVolumized(self):
	   start = time.time()
	   size =  self.db.find().count()-1 
	   print 'Item Count: %s' % size
	   db = self.db
	 #  try :  
	   for cursor, first in  enumerate(db.find(timeout= False)):
			if not self.hasGroupId(first):
				for idx,second in enumerate(db.find(timeout = False)):
					if first['key'] != second['key'] and self.objectMatch(first,second):
						#hasMatch = insertOrUpdate(first, second, db)
						second['matchscore'] = self.addScoreDictionary(second['name'],first['name'])
						if not self.hasExisting(self.memory, second) and not self.hasGroupId(second):
							second['groupid'] = self.stamp(first)
							self.memory.append(second)	
							print 'INSERTING :' +  second['groupid'] +' KEY ' + second['key'] 
							self.hasMatch = True		
						else:
							self.replaceBetterMatch(second, first)
			
					if  idx == size and self.hasMatch:
						print 'PARENT %s ' % first['key']					
						self.multiUpdate(self.memory)
						#self.updateInDb(self.memory[0])
						first['matchscore'] = 100
						first['rank'] = '1'	
						first['groupid'] = hashlib.md5(first['key']).hexdigest() 
						self.updateInDb(first)
						self.memory = []
						self.hasMatch = False 	
			print cursor
						
	   end = time.time()
	   print "feeding finisehd in %s ms"%(end-start)
	#assign score value to object
	def stamp(self,first):
		groupid = hashlib.md5(first['key']).hexdigest()
		return groupid

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
	def replaceBetterMatch(self, toAdd, first):
		if self.hasExisting(self.memory, toAdd):
			for item in self.memory:
				if item['site'] == toAdd['site']:
					if self.checkScore(item['matchscore'], toAdd['matchscore']):
						if self.compareOverallScores(item, toAdd):
							print 'higer replacement score for item ' + toAdd['key'] + 'vs ' + item['key'] + 'relative to ' + first['key']
							self.memory = [d for d in self.memory if d.get('site') != toAdd['site']]
							toAdd['groupid'] = self.stamp(first)
							self.memory.append(toAdd)


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
			
		if score1 < score2:
			return True
		elif score1 > score2:
			return False
		elif score1 == score2:
			return True				

	def objectMatch(self, first, second):
	#	if not hasGroupKey(second):
		try:
			if first['site'] != second['site']:
				if self.matchVolume(first['volume'], second['volume']):		
					if self.fuzzyMatchBrand(first['brand'], second['brand']):
						if self.matchName(first['name'], second['name']):
							a= first['key'] + 'and '+ second['key']	
							#if self.partialTokenCheck(first['name'], second['name']):
							return True
							#else:
							#	print a 
	
						else: 
							return False
					else:		
						return False
				else: 
					return False
			else:
				return False

		except Exception, e:
			logging.debug(e)		


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

	def fuzzyNameMatch(self, name1, name2):
		ratio = fuzz.token_set_ratio(name1,name2)	
		return ratio 

	def partialTokenMatch(self, name1,name2):
		ratio = fuzz.partial_token_sort_ratio(name1,name2)
		return ratio
	def partialTokenCheck(self, name1, name2):
		ratio = self.partialTokenMatch(name1,name2)
		if ratio > PARTIAL_TOKEN_SORT_RATIO:
			return True
		elif ratio < PARTIAL_TOKEN_SORT_RATIO:
			return False
		elif ratio == PARTIAL_TOKEN_SORT_RATIO:
			return True 
	
	def tokenSortMatch(self, name1, name2):
		ratio = fuzz.token_sort_ratio(name1,name2)
		return ratio
	def tokenCheck(self, name1, name2):
		ratio = self.tokenSortMatch(name1,name2)
		if ratio > TOKEN_SORT_RATIO:
			return True
		elif ratio < TOKEN_SORT_RATIO:
			return False
		elif ratio == TOKEN_SORT_RATIO:
			return False 

	def matchName(self, name1, name2):
		ratio = fuzz.token_set_ratio(name1,name2)	
		if ratio > NAME_RATIO:
			print 'RATIO:  %s' %ratio
			return True
		else:
			return False
			
	def checkVolume(self, vol1, vol2):
		if vol1 =='NA':
			return False
		else:
			if vol2 == 'NA':
				return False
			else:
				return True

	def matchVolume(self, vol1, vol2):

	  if self.checkVolume(vol1,vol2): 

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
	
	def updateInDb(self, item):
		
		self.db.update( {'key': item['key']}, item, safe = True)
		
	def multiUpdate(self, array): 
		try:
			for item in array:
				self.db.update( {'key' :item['key']} , item, safe = True)  
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
