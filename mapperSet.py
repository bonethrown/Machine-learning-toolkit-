from pymongo import Connection
from betaMapreduce import FuzzMatcher
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz
import hashlib
import logging
from nltk import regexp_tokenize, tokenwrap, word_tokenize
import string
import catChecker
import nltk.classify.util
from nltk import classify
from nltk.classify import NaiveBayesClassifier
import random
from dataOps import databaseManager
import re
from utils import listMatcher
COMMIT = True

INDB = 'neworder'
INCOLL = 'raw_January'	
OUTDB = 'neworder'
OUTCOLL = 'test_set'
FINAL_COLL = 'january_proccessed'
MAP_PATH = '/home/dev/kk_cosme/cosme/cosme/pipes/utils/brandmaptable.list'
match_path = '/home/dev/kk_cosme/cosme/cosme/pipes/utils/brandric.list'
#INDB is raw db rom crawlers
#OUTDB is cleaned data 
#OUTDB is split into 7 dbs by category after category matching
#matching is performed on seperate Dbs
#dbs are merged back into a single db

#databasemanager is the db connection class that handles all db related things

COMMENT_COLL = 'test'
logging.basicConfig(filename='matchLog.log', level=logging.DEBUG)

CATEGORY_LIST = ['perfume', 'unha', 'corpo e banho', 'acessorios', 'homem', 'maquiagem', 'cabelo']

class CleanAndCategorize(object):
	
	def __init__(self, launch_with_model = True):
		self.bayes = BayesObject()
		self.outdb = databaseManager(OUTDB, OUTCOLL, COMMENT_COLL)	
		self.indb = databaseManager(INDB, INCOLL, COMMENT_COLL)
		self.fuzz = FuzzMatcher(OUTDB, OUTCOLL)
		self.mapreduce = Mapreduce()
		self.init_Model(launch_with_model)
		self.norm = Normalize(OUTDB, OUTCOLL)
	def init_Model(self, toLoad = True):
		if toLoad:
			self.trainedmodel = self.bayes.makeModel()
	def reload(self):
		self.outdb = databaseManager(OUTDB, OUTCOLL, COMMENT_COLL)	
		self.indb = databaseManager(INDB, INCOLL, COMMENT_COLL)
		self.mapreduce = Mapreduce()
		self.bayes = BayesObject()
	def reloadModel(self):
		self.trainedmodel = self.bayes.makeModel()
 
	def Execute(self):
		### RED ME BEFORE RUNNING
			# FIRST DB IS IN TO CREATE OUTDB AS NOT TO MODIFY ORIGINAL DATA
			# SECOND COMMANDS RUN ON OUTDB 
		self.mapreduce.makeMappingCopy(self.indb.lalinaCollection, self.outdb.lalinaCollection)
		self.norm.brandReduce()	
		self.dumbClassify(self.outdb)
		#self.smartClassify(self.outdb)
		#print ' running Matcher this may take an hour'
		self.runMatcher()
		#### RUN MATCHER HERE ####
	def runMatcher(self):
		self.outdb.chop2cats(self.outdb.getCollection())
		self.fuzz.loopMatch()
		self.outdb.multiMerge(FINAL_COLL, self.outdb.catdbs)
			
	def dumbClassify(self, dbhandler):
		collection = dbhandler.getCollection()
		print 'db is: %s' % collection
		self.bayes.batchDumbClassify(collection)

	def smartClassify(self, dbhandler):
		collection = dbhandler.getCollection()
		for item in collection.find():
			if not item['category']:
				item['category'] = self.bayes.classify(self.trainedmodel, item)
				dbhandler.updateLalinaItem(item)

class Normalize(object):
	def __init__(self, db, coll):
		self.db = databaseManager(db, coll, coll)
		self.matcher = listMatcher(match_path)
		self.coll= self.db.getCollection()
		self.table = catChecker.Tables()
		self._map = self.table.buildCategoryTable(MAP_PATH)
	def brandNormalize(self, brand):
		match = self.matcher.listMatch(brand)			
		fuzz_match = self.matcher.fuzzMatch(brand)
		return match, fuzz_match	

	def dualmatch(self, brand):
		out = self.matcher.dualMatch(brand)
		return out
	
	def brandReduce(self):
		count = 0 
		for item in self.coll.find():
			brand = unicode(item['brand'])
			for element in self._map:
				key = element.keys()
				key = key[0]
				arr=  element.values()		
				arr= arr[0]	#return brand
				if brand == key:
					pass
						#print 'IN: %s    OUT: %s' % (brand,key)
				elif brand in arr:
					#print 'IN : %s MATCH: %s KEY: %s' % (brand,element.values(), key)
					item['brand'] = key
					count = count + 1
					self.db.updateLalinaItem(item)
				#else:
				#	return brand
		print 'REDUCED: %s' % count

	def getCatRow(self, category):
                catList = []
                arr = []
                for item in self._map:
                        for key, value in item.iteritems():
                                if key == category:
                                        catList.extend(value)
                                        catList.append(unicode(category))

                return catList
	
	def batchnormalize(self):
		total = self.coll.count()
		print total
		nomatch = []
		count = 0 
		_count = 0
		for item in self.coll.find():
			_count = _count + 1
			print _count
			brand  = self.dualmatch(item['brand'])
			if brand:
				item['brand'] = brand
			else:
				count = count + 1
				nomatch.append(item['url'])
		print 'nomatch: %s from total ; %s ' % (count, total)
	
class Name(object):
	
	def __init__(self, string):	
		self.name = string.lower()
		self.hasMatch = False	
		self.matches = []
		self.url = ""
		self.des = ""
	def makeUnicode(self, string):
		if not isinstance(string, unicode):
			string = string.encode('utf-8')
			return string
		else:
			return string
	def getNameDes(self):
		return " ".join([self.name,self.des])	
	def get(self):
		return self
	
	def unigram(self, name):
		name = self.makeUnicode(self.name)
		return  name.split()
	def bigram(self, name):
		input_list = self.unigram(name)
	  	return zip(input_list, input_list[1:])
	def trigram(self, name):
		input_list = self.unigram(name)
		return zip(input_list, input_list[1:], input_list[2:])
	def grams(self):
		unigram = self.unigram(self.name)
		bigram = self.bigram(self.name)
		trigram = self.trigram(self.name)
			
		unigram.extend(bigram)
		unigram.extend(trigram)
	
		out = []
		for term in unigram:
			if isinstance(term, tuple):
				lookup = " ".join(map(unicode, term))
				out.append(lookup)	
			else:
				lookup = term	
				out.append(lookup)	
		return out
	def matched(self, synList):
		ngrams = set(self.grams())
		matched = []
		for item in synList:
			for gram in ngrams:
				if item == gram:
					matched.append(gram)				
		matched = list(set(matched))
		return matched
	def input_featurize(self, tokens):
		words = [w for w in self.unigram(tokens)] 	
		uniq = set(words)
		features = dict()
		for word in words:
			features[word] = (word in uniq)
		return features
	def customFeaturize(self, word):
		# call with name object	
		words = []
		words.append(word) 	
		uniq = set(words)
		features = dict()
		for word in words:
			features[word] = (word in uniq)
		return features
	def featurize(self):
		# call with name object	
		words = [w for w in self.unigram(self.name)] 	
		uniq = set(words)
		features = dict()
		for word in words:
			features[word] = (word in uniq)
		return features
	
class ReverseLookup(object):
	
	def __init__(self):
		self.ngrammer = Ngrammer()
		

	def keyWord(self, namestr):
		name = Name(namestr)
		categories = self.ngrammer.categories()	
		
		for cat in categories:
			doc = name.matched(self.ngrammer.getCatRow(cat))
		# LOOP WILL RUN AND WILL MATCH THE LAST ONE IT FINDS THIS COULD BE A PROBLEM AND NEEDS VERIFICATION
			if doc:
				return doc
	
class BayesObject(object):

	def __init__(self):
		self.matched = []
		self.unmatched = []
		self.handler = DatabaseHandler()
		self.ngrammer = Ngrammer()
		self.corpus = self.allNames()
	#	self.model = self.makeModel()
	#creates the name object for each string name
	def loadCorpus(self, arr):
		out = []
		for item in arr:	
			_name = self.convertItem(item)
			out.append(_name)
		return out

	def allNames(self):
		out = []
		for item in self.handler.indb.find():
			_name = self.convertItem(item)
			out.append(_name)
		return out
	#used to refresh the databas or switch to another database withoud killing the object		
	def initdatabase(self, db, coll):
		self._handler = databaseManager(db,coll,coll)
		self.db = self._handler.getCollection()
		print 'Bayes DB: %s ' % self.db
	
	def convertItem(self, item):
		name = item['name']
	
		url = item['url']
		des = item['description']
		_name = Name(name)
		_name.url = url
		_name.volume  = item['volume']
		_name.brand = item['brand']
		_name.cat = item['category']
		_name.url = url
		
		_name.des = des
		return _name
	#match a single ITEM to a category
	def singleMatch(self, item):
			
		_name = self.convertItem(item)
		category = self.matchOne(_name)
		return category
	#run a dumbclassification on a database
	def batchDumbClassify(self, db):
		
		categories = self.ngrammer.categories()
		for item in db.find():
			name = self.convertItem(item)
			isMatched = False
			for cat in categories:
				doc = name.matched(self.ngrammer.getCatRow(cat))
				if doc:
					#print "DUAL MATCH: %s, cat1: %s, cat2: %s" % (name.name, mem, cat)
					#print 'Match name: %s, match: %s, cat: %s' % (name.name, doc, cat)
					if not isMatched:
						item['category'] = cat
						self.handler.updateInDb(dict(item), db)
						#print 'match is : %s' % cat
						#dic = name.featurize()
						#tup = (dic, cat)
						#matched.append(tup)
					isMatched = True
			#if not isMatched:
			
				
	#training match set for item matching	#return matched, unmatched
	def lalinaMatchTrainSet(self, db, category):
		matched = []
		unmatched = []
		for item in db.find({ 'category' : category}):
			_name = self.convertItem(item)
			if 'matchscore' in item:
				groupid = item['groupid']
				dic_a = _name.featurize()
			        dic_b  = _name.customFeaturize(_name.brand)
				dic = dict(dic_a.items() + dic_b.items()) 	
				#dic_brand = _name.featurize()
				#dic_volume = _name.featurize()
				tup = (dic, groupid)
				matched.append(tup)
			else:
				
				unmatched.append(_name)
		return matched, unmatched

	#this is the DUMB classify method
	#returns to arrays to self, Unmatched and MATCHED
	#used for categorization
	#used mainly in shell to play around and see matched and unmatched array
	def garanti(self):
		unmatched = []
		matched = []
		
		categories = self.ngrammer.categories()
		print 'categories are : %s' % categories
		for name in self.corpus:
			isMatched = False
			for cat in categories:
				doc = name.matched(self.ngrammer.getCatRow(cat))
				if doc:
					#print "DUAL MATCH: %s, cat1: %s, cat2: %s" % (name.name, mem, cat)
					#print 'Match name: %s, match: %s, cat: %s' % (name.name, doc, cat)
					if not isMatched:
						dic = name.featurize()
						tup = (dic, cat)
						matched.append(tup)
					isMatched = True
			if not isMatched:
			
				unmatched.append(name)	
				
		return matched, unmatched
	#category match a single item expects name object
	def matchOne(self, nameObject):
		name = nameObject
		categories = self.ngrammer.categories()	
		
		for cat in categories:
			doc = name.matched(self.ngrammer.getCatRow(cat))
		# LOOP WILL RUN AND WILL MATCH THE LAST ONE IT FINDS THIS COULD BE A PROBLEM AND NEEDS VERIFICATION
			if doc:
				return cat
	
	#standard model for categorization	
	def makeModel(self):
		self.matched, self.unmatched = self.garanti()
		random.shuffle(self.matched)
		model = NaiveBayesClassifier.train(self.matched[:1500])
		return model			
	#experimental model to extend ML to  ITEM MATCHING 
	def makeMatchModel(self, db, category):	
		self.matched, self.unmatched= self.lalinaMatchTrainSet(db, category)
		random.shuffle(self.matched)
		model = NaiveBayesClassifier.train(self.matched[:400])
		return model			
	#classify via ML must recieve a NAME object
	def nameobj_classify(self, model, _name):
		tokens = _name.name + name.brand
		classified = NaiveBayesClassifier.classify(model, _name.input_featurize(tokens))	
		return classified
	#classify for ML, expects an Item and converts it onto name object
	#This is used to run via mogodb collection.find() loop
	def classify(self, model, item):
		_name = self.convertItem(item)
		tokens = _name.getNameDes()
		classified = NaiveBayesClassifier.classify(model, _name.input_featurize(tokens))	
		return classified
	#batch classify the unmatched array 
	def batchClassify(self, model):
		for item in self.unmatched:
			classified = NaiveBayesClassifier.classify(model, item.featurize())	
			#print 'cat is: %s, name: %s, url: %s' % (classified, item.name, item.url)

	def test(self):
		testArr= self.matched[100:]
		random.shuffle(testArr)
		for item in testArr:
			classified = NaiveBayesClassifier.classify(self.model,item)	

##### SOME PARETS OF THIS IS LEGAVY AND NEEDS REFINING BUT SOME PARTS USED SEE ABOVE 12/13

class Ngrammer(object):
	
	def __init__(self):
		
		self.test_list = ['all', 'this', 'hayyppened', 'more', 'or', 'less']
		#self.handler = DatabaseHandler()
		self.tables = catChecker.Tables()
	def makeUnicode(self, string):
		if not isinstance(string, unicode):
			string = string.encode('utf-8')
			return string
		else:
			return string
	def categories(self):
		return CATEGORY_LIST	
	
	def unigram(self, name):
		name = self.makeUnicode(name)
		return  name.split()

	def bigram(self, name):
		input_list = self.unigram(name)
	  	return zip(input_list, input_list[1:])
	def trigram(self, name):
		input_list = self.unigram(name)
		return zip(input_list, input_list[1:], input_list[2:])
	
	def buildGrams(self, name):
		unigram = self.unigram(name)
		bigram = self.bigram(name)
		trigram = self.trigram(name)
			
		unigram.extend(bigram)
		unigram.extend(trigram)
	
		out = []
		for term in unigram:
			if isinstance(term, tuple):
				lookup = " ".join(map(unicode, term))
				out.append(lookup)	
			else:
				lookup = term	
				out.append(lookup)	
		return out
	# JUST A UTILITY FUNCTION TO CHECK IF NON VOLUME CATEGORIES HAVE VOLUME
	def extractTupleList(self, field1 = 'grams', field2 = 'category'):
		arr = []
		for item in self.outdb.find():
			tup = (item[field1] , item[field2])
			arr.append(tup)
		return arr

	def uniProbDist(self, coll):
		uniArray = []
		wordcount = 0
		for item in coll.find():
			name = self.unigram(item['name'])
			uniArray.extend(name)
			b = len(name)
			wordcount = wordcount + b
		return uniArray
	
	def biProbDist(self, coll):
		biArray = []
		wordcount = 0
		for item in coll.find():
			name = self.bigram(item['name'])
			biArray.extend(name)
			b = len(name)
			wordcount = wordcount + b
		return biArray

	def triProbDist(self, coll):
		triArray = []
		wordcount = 0
		for item in coll.find():
			name = self.trigram(item['name'])
			triArray.extend(name)
			b = len(name)
			wordcount = wordcount + b
		return triArray
	
	def uniqueGrams(self, arr):
		out = set(arr)
		return out
	
	def getCatRow(self, category):
		catList = []
		arr = []
		for item in self.tables.catTable:
			for key, value in item.iteritems():
				if key == category:
					catList.extend(value)
					catList.append(unicode(category))

		return catList
	

	def uniMatch(self, termArr, categoryString):
		count = 0
		catArr = self.getCatRow(categoryString)	
		matches = []
		for term in termArr:
			for cat in catArr:
				if term == cat:
					tup = (term, categoryString)
					matches.append(tup)
					count = count +1
		print 'total matches: %s' % len(matches) 
		return matches


	def ngramMatch(self, tuppleTermArr, categoryString):
		
		catArr = self.getCatRow(categoryString)
		count = 0
		matches = []	
		for term in tuppleTermArr:
			if isinstance(term, tuple):
				lookup = " ".join(map(unicode, term))
			else:
				lookup = term	

			for cat in catArr:
				if lookup == cat:
					count = count + 1
					tup = (lookup, categoryString)
					matches.append(tup)
			
		print 'total in match arr: %s' % len(matches)
		return matches
	

	def allCatMatch(self):
		
		unigramArr = self.uniProbDist()
		bigramArr = self.biProbDist()
		trigramArr = self.triProbDist()
		unigramArr.extend(bigramArr)
		unigramArr.extend(trigramArr)
		
		categoryList = ['perfume', 'unha', 'corpo e banho', 'acessorios', 'homem', 'maquiagem', 'cabelo']
		catsList = []
		for cat in categoryList:
			print 'matching cat: %s' % cat

			catsList.extend(self.ngramMatch(unigramArr, cat))
		print 'all matches in list: %s' % len(catsList)

		return catsList	

	def catProb(self, categoryString):
		unigramArr = self.uniProbDist()
		bigramArr = self.biProbDist()
		trigramArr = self.triProbDist()
		
		totalUnigrams = len(unigramArr)
		totalBigrams = len(bigramArr)
		totalTrigrams = len(trigramArr)
	
		print 'total unigrams: %s, bigrams: %s, trigrams: %s' % (totalUnigrams, totalBigrams, totalTrigrams)

		probUni = len(self.ngramMatch(unigramArr, categoryString))
		probBi = len(self.ngramMatch(bigramArr, categoryString))
		probTri = len(self.ngramMatch(trigramArr, categoryString))	
		
		print 'total uni matches %s, total bi matches: %s, total tri matches: %s' % (probUni, probBi, probTri)
		
		pUni = float(probUni) / float(totalUnigrams)
		pBi = float(probBi) / float(totalBigrams)
		pTri = float(probTri) / float(totalTrigrams)
		
		return pUni, pBi, pTri


	def document_features(self, document): # [_document-classify-extractor]
	    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
	    word_features = all_words.keys()[:100] # [_document-classify-all-words]
	    document_words = set(document) # [_document-classify-set]
	    features = {}
	    for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	    return features


###################
####DEPRECEATED USE DATAOPs.PY
###############################
################################
###############################

class DatabaseHandler(object):
	def __init__(self):
		self.connection = Connection()
		self.indb = self.connection[INDB]
		self.indb = self.indb[INCOLL]
		outdb = Connection()
		outdb = outdb[OUTDB]
		self.outdb = outdb[OUTCOLL]

	def updateInDb(self, item, db):
		try:
			db.save(item)
		
		except Exception, e:
			print 'mongo exception'
		
	def updateFieldInDb(self, item, field, db):

		try:
			db.save(item['key'], item[field])
		
		except Exception, e:
			print 'mongo exception'
	
	def insertToDb(self, item, db):
		try:
			db.insert(item, safe=True)
		
		except Exception, e:
			print 'mongo exception'

class Mapreduce(object):

	def __init__(self):
		self.pattern = r'(?x)\n  ([A-Z]\\.)+  \n | \\w+(-\\w+)*\n| \\$?\\d+(\\.\\d+)?%?\n| \\.\\.\\.\n| [][.,;"\'?():-_`]\n'
		# this cleans all punction
		self.volPattern = r'''(?i) \d+ml|\d+ ml|\d+ML|\d+ML|\d+g|\d+ g|\d+gr|\d+ gramas|\d+ gr|\d+gramas'''
		#converts voluem types to generic types
		self.mem = []

	def pricePerVolume(self, item):
			if item['volume'] != 'na':
				try:
					number = re.search(r'\d+', item['volume'])
					if number:
						number = number.group()
						volume = float(number)
						price = item['price']
						price = price[0]
						volume = float(number)
						costPerVol = float(price)/ float(volume)
						costPerVol = round(costPerVol, 2)
						return costPerVol
					else:
						return 'NA'
				except Exception, e:
					print 'PRice per volume error: %s, item: %s ' % (e, item['key'])

			return item[field]

	def checkPrice(self, item):
		price = item['price'][0]
		key = item['key']
		if not item['price'] == 'NA':
			if isinstance(price, float):
			 	pass
			else:
				print 'Price not Float: %s : key %s' % (price, key)
	
	def makeMappingCopy(self, indb, outdb):
		print 'INDB is %s' % indb
		print 'OUTDB is %s' % outdb
		logdump = []
		logName = ''
		for item in indb.find():
			if 'name' in item:
				#try:
					copyObject = item 
					#copyObject = self.lowerfields(copyObject) 
					newName = self.cleaner(copyObject['name'])
					newBrand = self.punctuationStripper(copyObject['brand'])
					#newCategory = self.cleaner(copyObject['category'])
					
						#toMem = 'name: '+ newName+', brand: '+newBrand 
						#self.mem.append(toMem)
					#copyObject['price'] = self.fieldScrubber(copyObject, 'price')
					copyObject['price_str'] = self.floatPriceToString(item['price'])		
					
					copyObject['volume'] = self.cleanSingleVolume(copyObject['volume'])
					copyObject['volume'] = self.removeAllSpaces(copyObject['volume'])
					copyObject['brand'] = newBrand
					copyObject['name'] = newName
					copyObject['price_per_vol'] = self.pricePerVolume(copyObject)
					copyObject['key'] = item['key']
					copyObject['category'] = ''
					self.checkPrice(copyObject)
					#cat is set to empty as matcher will do a pass afterwards then machine learning
					
					self.insertToDb(copyObject, outdb)	
		

		#self.updateInDb(self.mem.append)
		print ' error : %s ' % len(self.mem)
		print 'start count: %s' % indb.count()
		print 'coppied %s' % outdb.count()
		self.writeToFile(self.mem, 'emptycat.list')
		self.writeToFile(logdump, 'validate_'+logName)
		self.mem = []
 		
	def cleanVolume(self, name):
		replaceList = regexp_tokenize(name, self.volPattern)
		crop = name
		if len(replaceList) > 0:
			for val in replaceList:
				crop = crop.replace(val, "")	
			crop = crop.strip()
			return crop
		else:
			return crop
 	def cleanSingleVolume(self, field):	
		if field is None:
			field = 'NA'
		if field == '':
			field = 'NA'
		elif len(field) == 0:
			field = 'NA'
		elif field == ['NA']:
                        field = 'NA'
		return field.lower()
	
	def batchCleanVolume(self, db):
                for item in db.lalinaCollection.find():
                        if item['volume'] is None:
                                item['volume'] = 'NA'
				db.updateLalinaItem(item)
                        if item['volume'] == '':
                                item['volume'] = 'NA'
				db.updateLalinaItem(item)
                        elif len(item['volume']) == 0:
                                item['volume'] = 'NA'
				db.updateLalinaItem(item)
                        elif item['volume'] == ['NA']:
                                item['volume'] = 'NA'
				db.updateLalinaItem(item)

	def removeMidWhiteSpaces(self, name):
		name = re.sub(r'\s+', ' ', name)
		return name	
	
	def punctuationStripper(self, string):
		phrase = string.strip()
		phrase = phrase.split(' ')
		out = []
		for item in phrase:
			a = ''.join(e for e in item if e.isalnum())
			out.append(a)
		out = ' '.join(out)
		return out

	def cleanName(self, name):
		exclude = set(string.punctuation)
		out = ''.join(ch for ch in name if ch not in exclude)				
		
		return out

	def quickExpand(self, name):
		r = r'edt|edp|c/|p/|eau de parfum|homme'
		expanddict = { 'p/':'para','c/':'com','edt' : 'eau de toilette', 'edp': 'eau de perfume','eau de parfum':'eau de perfume','homme':'masculino' }
		a = re.search(r, name)
		if a is not None:
			a = a.group()
			for keys in expanddict:
				if keys == a:
					name = name.replace(a, expanddict[keys])
					return name
		else:
			return name
			
	def dupRemove(self, a):	
		a = ' '.join(self.unique_list(a.split()))
		return a

	def unique_list(self, l):
		ulist = []
    		[ulist.append(x) for x in l if x not in ulist]
    		return ulist 
		
	def fieldScrubber(self, item, fieldToClean):
		

		if not item[fieldToClean]:
			return 'NA'
		elif item[fieldToClean] == None:
			print 'OOPS None price scrubber: %s ' % item['key']
			return 'NA'
		elif len(item[fieldToClean]) == 0:
			return 'NA'
		elif item[fieldToClean] == ['NA']:
			return 'NA'
		else:
			return item[fieldToClean]
	# USED TO CLEAN NAME FIELD
	def cleaner(self, newName):
		#ORDER IMPORTTAN
		if not isinstance(newName, unicode):
			newName = newName.decode('utf8')
		newName = newName.lower()
		newName = self.quickExpand(newName)
		newName = self.punctuationStripper(newName)
		newName = self.cleanName(newName)
		newName = self.cleanVolume(newName)
		newName = self.removeMidWhiteSpaces(newName)
		newName = self.dupRemove(newName)
		newName = self.removeMidWhiteSpaces(newName)
		return newName
	
	def removeAllSpaces(self, string):
		return "".join(string.split())

	def floatPriceToString(self, priceFloat):
		if isinstance(priceFloat, list):
			if priceFloat != 'NA':	
				priceFloat = priceFloat[0]
				try:
					pricestr = '%.2f' % float(priceFloat) 
					return pricestr
				except Exception, e:
					print e
					return priceFloat
				
		else:
			if priceFloat != 'NA':
				print priceFloat
				pricestr = '%.2f' % priceFloat 
				return pricestr
			else:
				return priceFloat		

	def patchDeadArrayToString(self, field):
		if isinstance(field, list) and not field:
			fix = ''
			return fix
		else:
			return field
	
	def arrayToString(self, field):
		if isinstance(field, list) and field:
			out = field[0]
			return out
		else:
			return field
	def arrayFixer(self, field):
		field = self.patchDeadArrayToString(field)
		field = self.arrayToString(field)
		return field

	def lowerfields(self, item):
		l = ['volume','product_id','matchscore','image','comments','price','date_crawled','_id', 'matchscore', 'rank', 'sku']
		uniq = set(l)
		for key, value in item.items():
			if not key in uniq:
					if isinstance(value, list):
						item[key] = self.arrayFixer(value)	
						print item[key]
					if value is not None:
						item[key] = item[key].lower().strip()
					else:
						value = ''
		return item

	def writeToFile(self, arr, logname):
	
		savedoc = open(logname+'.log','wb')
		for a in arr:
			savedoc.write("%s\n" % a.encode('utf8'))
		savedoc.close()

	def writeTuple(self, temp):
		savedoc = open('errorlogmap', 'wb')
		for a in temp:
			savedoc.write("%s\n" % a[0].encode('utf-8'), a[1].encode('utf-8'))		
		savedoc.close()
	
	def updateMongo(self, item, db):
		try:
			db.update({'key':item['key']}, {'$set': { 'groupid': item['groupid'] } }, upsert = True) 
		
		except Exception, e:
			print 'mongo exception'
		
	def updateInDb(self, item, field, db):

		try:
			db.save(item['key'], item[field])
		
		except Exception, e:
			print 'mongo Update exception'

	
	def insertToDb(self, item, db):
			
		try:
			db.insert(item)
		
		except Exception, e:
			print 'mongo Insertion exception'
		
	def main(collection):
		connection = Connection()
		db = connection[OUTDB]
		db = db[collection]
		print 'collection in use %s' %db
