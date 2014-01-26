from pymongo import Connection
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz
import hashlib
import logging
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
USE_VOL = True

class fuzzMatcher(object):

	def __init__(self, db= MAINDB, collection= COLLECTION):
		self.tables = Tables() 
		self.handler = databaseManager(db, collection,collection)
		self.stopwords = self.filterStopWords('stopwords.list')
		self.memory = []
		self.hasMatch = False
	def loopDbMatch(self):

		for db in self.handler.catdbs:
			print 'working Db : %s' % db
			self.matchVolumized(db)
		
	def settings(self, stringCategory):
		if stringCategory == 'perfume':
			settings = {'name_ratio' : 92,
					'partial_ratio' : 70,
					'token_ratio' : 75,
					} 
			return settings
		elif stringCategory == 'cabelo':
			settings = {'name_ratio' : 92,
					'partial_ratio' : 70,
					'token_ratio' : 75,
					} 
			return settings
		elif stringCategory == 'unha':
			settings = {'name_ratio' : 92,
					'partial_ratio' : 70,
					'token_ratio' : 75,
					} 
			return settings
		elif stringCategory == 'cabelo':
			settings = {'name_ratio' : 92,
					'partial_ratio' : 70,
					'token_ratio' : 75,
					} 
			return settings
		elif stringCategory == 'corpo e banho':
			settings = {'name_ratio' : 92,
					'partial_ratio' : 70,
					'token_ratio' : 75,
					} 
			return settings
		elif stringCategory == 'acessorios':
			settings = {'name_ratio' : 92,
					'partial_ratio' : 70,
					'token_ratio' : 75,
					} 
			return settings
		elif stringCategory == 'homem':
			settings = {'name_ratio' : 92,
					'partial_ratio' : 70,
					'token_ratio' : 75,
					} 
			return settings

	def singleMatch(self):
		self.matchVolumized(self.handler.getCollection())
			
		print 'check test collection %s for results' % collection 
	def filterStopWords(self,stopFile):
		stopList = self.tables.commaFileToList('stopwords.list')	
		#filtered = res = [k for k in lst if 'ab' in k]	
		return stopList

	
	def stopfilter(self, name):
		name = name.decode('utf-8')
		name = name.split()
		filtered = [k for k in name if not k in self.stopwords]
		out =" ".join(filtered)
		return out
	def keycheck(self, key1,key2):
		if key1 == key2:
			return False
		else:
			return True

	
	def  matchVolumized(self, selected_db):
	   self.memory = []	
	   db = selected_db
	   start = time.time()
	   size =  db.find().count()-1 
	   print db
	   print 'Item Count: %s' % size
	 #  try :  
	   for cursor, first in  enumerate(db.find(timeout= False)):
			#if not self.hasGroupId(first):
			if cursor:
				for idx,second in enumerate(db.find(timeout = False)):
					#print 'first['key']
					keycheck = self.keycheck(first['key'], second['key'])
					match = self.objectMatch_avg(first, second)
					if keycheck and match:
						#hasMatch = insertOrUpdate(first, second, db)
						second['matchscore'] = self.addScoreDictionary(second['name'],first['name'])
						#print second['matchscore']
						if not self.hasExisting(self.memory, second) and not self.hasGroupId(second):
							print 'HAS MATCH'
							self.memory.append(second)	
							second['groupid'] = self.stamp(first)
							self.hasMatch = True		
							print 'INSERTING GROUPID:' +  second['groupid'] +' KEY ' + second['key'] 
						else:
							self.replaceBetterMatch(second, first)
			
					if  idx == size and self.hasMatch:
						self.multiUpdate(self.memory, db)
						#self.updateInDb(self.memory[0])
						first['rank'] = '1'	
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
	def replaceBetterMatch(self, toAdd, first):
		if self.hasExisting(self.memory, toAdd):
			for item in self.memory:
				if item['site'] == toAdd['site']:
					if self.checkScore(item['matchscore'], toAdd['matchscore']):
						if self.compareOverallScores(item, toAdd):
							print 'higer replacement score for item ' + toAdd['key'] + 'vs ' + item['key'] + ' parent ' + first['key']
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
			
		if score1 < score2:
			return True
		elif score1 > score2:
			return False
		elif score1 == score2:
			return True				

	def objectMatch_avg(self, first, second):
		if first['site'] != second['site']:
			if self.fuzzyMatchBrand(first['brand'], second['brand']):
				vol_match = self.matchVolume(first['volume'], second['volume'])
				if USE_VOL:
					if vol_match:
						score = self.avgScoreMatch(first['name'],second['name'])
						return score
					else:
						return False 	
				else:
					score = self.avgScoreMatch(first['name'],second['name'])
					return score 	
			else:
				return False	
		else:
			return False
									

	def objectMatch(self, first, second):
	#	if not hasGroupKey(second):
		try:
			if first['site'] != second['site']:
				if self.matchVolume(first['volume'], second['volume']):		
					if self.fuzzyMatchBrand(first['brand'], second['brand']):
						match, score = self.matchName(first['name'], second['name'])
						if match:
							
							tri = self.triFuzzyMatch(first['name'], second['name'])
							print ' 0##: %s ' %tri 
							tri = self.triFuzzyMatch(self.stopfilter(first['name']), self.stopfilter(second['name']))
							print ' 1^^: %s ' % tri
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
	def avgScoreMatch(self, name1, name2):
		score  = self.triFuzzyMatch(name1,name2)
		name = score['nameratio']
		part = score['partial']
		token = score['token']

		total =  float(name) + float(part) + float(token)
		avg = float(total) / 3
		#print 'avg score : %s total score : %s ' % (avg, total)
		if avg >= AVG_THRESH:
			return True
		else:
			return False


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
