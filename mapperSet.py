from pymongo import Connection
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz
import hashlib
import logging
from cosme.pipes.utils import utils
from nltk import regexp_tokenize, tokenwrap, word_tokenize
import re
import string
import catChecker
import nltk.classify.util
from nltk import classify
from nltk.classify import NaiveBayesClassifier
from catChecker import FieldCreator 
import random
from cosme.dataOps import databaseManager

COMMIT = True

INDB = 'production'
INCOLL = 'lalina1018'	
OUTDB = 'matching'
OUTCOLL = 'la1018'

TESTDB = 'matching'
TESTCOLL = 'unittest'
COMMENT_COLL = 'test'
logging.basicConfig(filename='matchLog.log', level=logging.DEBUG)

CATEGORY_LIST = ['perfume', 'unha', 'corpo e banho', 'acessorios', 'homem', 'maquiagem', 'cabelo']

class CleanAndCategorize(object):
	
	def __init__(self):
		self.handler = DatabaseHandler()
		self.mapreduce = Mapreduce()
		self.bayes = BayesObject()
		self.trainedmodel = self.bayes.makeModel()
		self._handler = databaseManager(OUTDB, OUTCOLL, COMMENT_COLL)	

	def reload(self):
		self._handler = databaseManager(OUTDB, OUTCOLL, COMMENT_COLL)	
		self.mapreduce = Mapreduce()
		self.bayes = BayesObject()
	def reloadModel(self):
		self.trainedmodel = self.bayes.makeModel()
		
 
	def runFieldCleaner(self):
		### RED ME BEFORE RUNNING
			# FIRST DB IS IN TO CREATE OUTDB AS NOT TO MODIFY ORIGINAL DATA
			# SECOND COMMANDS RUN ON OUTDB 
		self.mapreduce.makeMappingCopy(self.handler.indb, self.handler.outdb)
		#self.mapreduce.batchCleanVolume(self.handler.outdb)
		#self.mapreduce.addStringPrice(self.handler.outdb)
		#self.bayes.batchDumbClassify(self.handler.outdb)
	def dumbClassify(self):
		self.bayes.batchDumbClassify(self._handler.lalinaCollection)

	def smartClassify(self):
		for item in self._handler.lalinaCollection.find():
			if not item['category']:
				item['category'] = self.bayes.classify(self.trainedmodel, item)
				self._handler.updateLalinaField(item, 'category')

	
class Name(object):
	
	def __init__(self, string):	
		self.name = string
		self.hasMatch = False	
		self.matches = []
		self.url = ""
	def makeUnicode(self, string):
		if not isinstance(string, unicode):
			string = string.encode('utf-8')
			return string
		else:
			return string
	
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
	def featurize(self):
		# call with name object	
		words = [w for w in self.unigram(self.name)] 	
		uniq = set(words)
		features = dict()
		for word in words:
			features[word] = (word in uniq)
		return features
	

class BayesObject(object):

	def __init__(self):
		self.matched = []
		self.unmatched = []
		self.handler = DatabaseHandler()
		self.ngrammer = Ngrammer()
		self.corpus = self.allNames()
	#	self.model = self.makeModel()
	#creates the name object for each string name
	def assignDBhandler(self, dbhandlerObject):
		self.handler = dbhandlerObject
 
	def allNames(self):
		out = []
		for item in self.handler.indb.find():
			
			name = item['name']
			url = item['url']
			_name = Name(name)
			_name.url = url
			out.append(_name)
		return out		

	def convertItem(self, item):
		name = item['name']
		url = item['url']
		_name = Name(name)
		_name.url = url
		return _name

	def singleMatch(self, item):
			
		_name = self.convertItem(item)
		category = self.matchOne(_name)
		return category

	def batchDumbClassify(self, db):
		
		categories = self.ngrammer.categories()
		print 'categories are : %s' % categories
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
			
				
		#return matched, unmatched

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

	def matchOne(self, nameObject):
		name = nameObject
		categories = self.ngrammer.categories()	
		
		for cat in categories:
			doc = name.matched(self.ngrammer.getCatRow(cat))
		# LOOP WILL RUN AND WILL MATCH THE LAST ONE IT FINDS THIS COULD BE A PROBLEM AND NEEDS VERIFICATION
		
		if doc:
			return cat
			
	def makeModel(self):
		self.matched, self.unmatched = self.garanti()
		random.shuffle(self.matched)
		model = NaiveBayesClassifier.train(self.matched[:1500])
		return model			
	

	def classify(self, model, item):
		_name = self.convertItem(item)
		classified = NaiveBayesClassifier.classify(model, _name.featurize())	
		return classified
	
	def batchClassify(self):
		for item in self.unmatched:
			classified = NaiveBayesClassifier.classify(self.model, item.featurize())	
			print 'cat is: %s, name: %s, url: %s' % (classified, item.name, item.url)

	def test(self):
		testArr= self.matched[100:]
		random.shuffle(testArr)
		for item in testArr:
			classified = NaiveBayesClassifier.classify(self.model,item)	

##### SOME PARETS OF THIS IS LEGAVY AND NEEDS REFINING BUT SOME PARTS USED SEE ABOVE 12/13

class Ngrammer(object):
	
	def __init__(self):
		
		self.test_list = ['all', 'this', 'hayyppened', 'more', 'or', 'less']
		self.handler = DatabaseHandler()
		self.tables = catChecker.Tables()
		self.creator = FieldCreator()
		
	def categories(self):
		return CATEGORY_LIST	
	
	def unigram(self, name):
		name = self.creator.makeUnicode(name)
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

	def uniProbDist(self):
		uniArray = []
		wordcount = 0
		for item in self.handler.indb.find():
			name = self.unigram(item['name'])
			uniArray.extend(name)
			b = len(name)
			wordcount = wordcount + b
		return uniArray
	
	def biProbDist(self):
		biArray = []
		wordcount = 0
		for item in self.handler.indb.find():
			name = self.bigram(item['name'])
			biArray.extend(name)
			b = len(name)
			wordcount = wordcount + b
		return biArray

	def triProbDist(self):
		triArray = []
		wordcount = 0
		for item in self.handler.indb.find():
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
		
		self.handler = DatabaseHandler()
		self.indb = self.handler.indb
		self.outdb = self.handler.outdb
		self.mem = []
	

	def addStringPrice(self, db):
		print 'INDB is %s' % db
		for item in db.find():
			try:
				copyObject = item 
				copyObject['price_str'] = self.floatPriceToString(item['price'])		
				self.updateInDb(copyObject)	
			except Exception, e:
				print e
				self.mem.append(item['key'])
				print item['key']	

	
	def makeMappingCopy(self, indb, outdb):
		print 'INDB is %s' % indb
		print 'OUTDB is %s' % outdb
		logdump = []
		logName = ''
		for item in indb.find():
			if 'name' in item:
				#try:
					copyObject = item 
					self.lowerfields(copyObject) 
					newName = self.cleaner(copyObject['name'])
					newVolume = self.remVolWhiteSpace(copyObject['volume'])
					newBrand = self.punctuationStripper(copyObject['brand'])
					#newCategory = self.cleaner(copyObject['category'])
					
					#print 'START'
					#print 'INCOMING Name IS: %s' % newName
					#print 'LOOP DONE, CAT OUT IS: %s' % copyObject['category']

						#toMem = 'name: '+ newName+', brand: '+newBrand 
						#self.mem.append(toMem)
							
					copyObject['brand'] = newBrand
					copyObject['price_str'] = self.floatPriceToString(item['price'])		
					copyObject['volume'] = self.fieldScrubber(item, 'volume')
					copyObject['name'] = newName
					copyObject['key'] = item['key']
					copyObject['category'] = ''
					#cat is set to empty as matcher will do a pass afterwards then machine learning
					
					self.insertToDb(copyObject, outdb)	
		

		#self.updateInDb(self.mem.append)
		print ' error : %s ' % len(self.mem)
		print 'start count: %s' % indb.count()
		print 'coppied %s' % outdb.count()
		self.writeToFile(self.mem, 'emptycat.list')
		self.writeToFile(logdump, 'validate_'+logName)
		self.mem = []	
	def stampDummyKey(self):
	#this is needed for solr to group things by groupid.
		counter = 0 
		toPatch = self.outdb.find({ 'groupid': { '$exists': 0}}).count()
		for item in self.outdb.find({ 'groupid': { '$exists': 0}}):
			if not 'groupid' in item:
				item['groupid'] =self.dummyGroupKey(item)
				self.updateMongo(item, self.outdb)				
				counter = counter+ 1
		print 'items patched: %s ' % counter
		print 'items needed patching %s ' %toPatch
 		
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

	def batchCleanVolume(db):
                for item in db.find():
                        print item['volume']
                        if item['volume'] is None:
                                item['volume'] = 'NA'
                                toDb(item,db)
                                print 'was None %s' % item['key']
                        if item['volume'] == '':
                                item['volume'] = 'NA'
                                toDb(item,db)
                                print 'item was empty string %s' % item['key']
                        elif len(item['volume']) == 0:
                                item['volume'] = 'NA'
                                toDb(item,db)
                                print 'item was empty ARRAY %s' % item['key']
                        elif item['volume'] == ['NA']:
                                item['volume'] = 'NA'
                                toDb(item,db)
                                print 'item was empty ARRAY %s' % item['key']

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
		
	def remVolWhiteSpace(self, vol):
		vol = "".join(vol.split())
		vol = vol.lower()
		return vol
	
	def fieldScrubber(self, item, fieldToClean):
		if item[fieldToClean] is None:
			return 'NA'
			print 'was None %s' % item['key']
		if item[fieldToClean] == '':
			return 'NA'
		elif len(item[fieldToClean]) == 0:
			return 'NA'
		elif item[fieldToClean] == ['NA']:
			return 'NA'

	def cleaner(self, newName):
		if not isinstance(newName, unicode):
			newName = newName.decode('utf8')
		newName = newName.lower()
		newName = self.quickExpand(newName)	
		newName = self.cleanVolume(newName)
		newName = self.cleanName(newName)
		newName = self.dupRemove(newName)
		newName = self.removeMidWhiteSpaces(newName)
		return newName

	def floatPriceToString(self, priceFloat):
		if isinstance(priceFloat, list):
			priceFloat = priceFloat[0]
			pricestr = '%.2f' % priceFloat 
			return pricestr
		else:
			pricestr = '%.2f' % priceFloat 
			return pricestr
			
	def dummyGroupKey(self, item):
		if not 'groupid' in item:
			groupid = '0000' + item['key']
			return groupid
		else:
			return item['groupid']

	def patchDeadArrayToString(self, field):
		if isinstance(field, list) and not field:
			fix = ''
			print 'patch done %s ' % field
			return fix
		else:
			return field
	
	def arrayToString(self, field):
		if isinstance(field, list) and field:
			print 'array element grab %s ' %field
			out = field[0]
			return out
		else:
			return field
	def arrayFixer(self, field):
		print 'fixer ran'
		field = self.patchDeadArrayToString(field)
		field = self.arrayToString(field)
		return field

	def lowerfields(self, item):
		l = ['product_id','matchscore','image','comments','price','date_crawled','_id', 'matchscore', 'rank', 'sku']
		uniq = set(l)
		for key, value in item.items():
			if not key in uniq:
					if isinstance(value, list):
						item[key] = self.arrayFixer(value)	
						print item[key]
					if value is not None:
						item[key] = item[key].lower().strip()
					else:
						print item[key]
						print key
						print '$$$$$$$$$$$$$$$ VALUE WAS NONE $$$$$$$$$$$$ %s' % item['key'] 
						value = ''

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
