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
logging.basicConfig(filename='matchLog.log', level=logging.DEBUG)
from fuzzywuzzy import fuzz
from copy import deepcopy

INDB = 'production'
INCOLL = 'lalina1018'
OUTDB = 'matching'
OUTCOLL = 'la1018'

TESTDB = 'matching'
TESTCOLL = 'unittest'

class Tables(object):
        def __init__(self):
                self.connection = Connection()

                self.indb = self.connection[INDB]
                self.indb = self.indb[INCOLL]

                outdb = Connection()
                outdb = outdb[OUTDB]
                self.outdb = outdb[OUTCOLL]
		
		testdb = Connection()
                testdb = testdb[TESTDB]
                self.testdb = testdb[TESTCOLL]
                #self.catTable = self.buildCategoryTable('category.list')
                #self.valTable = self.buildKeyTable(self.catTable)
                #self.catExtTable = self.buildCategoryTable('category.name')

                self.acc = self.buildCategoryTable('acessorios.list')
                self.cab = self.buildCategoryTable('cabelo.list')
                self.maq = self.buildCategoryTable('maquiagem.list')
                self.hom = self.buildCategoryTable('homem.list')
                self.cor = self.buildCategoryTable('corpo.list')
                self.unh = self.buildCategoryTable('unhas.list')
                self.per = self.buildCategoryTable('perfumes.list')

                #KEY TABLE
                self.catTable = self.buildTree()
                #self.valTable = self.buildKeyTable(self.catTable)
                #print self.acc
                #print self.cab

        def buildTree(self):
                tree = []
                tree.extend(self.acc)
                tree.extend(self.cab)
                tree.extend(self.maq)
                tree.extend(self.hom)
                tree.extend(self.cor)
                tree.extend(self.unh)
                tree.extend(self.per)
                return tree

        #THIS FUNCTION OUTPUTS ALL *UNIQUE FIELDS INTO A FILE. SUCH AS ALL UNQIUE BRANDS TO A SINGLE FILE.
        def fieldMapToFile(self, stringfield, collection):
                savedoc = open(stringfield+'map', 'wb')
                temp = []
                for item in collection.find():
                        if not any(item[stringfield] in s for s in temp):
                                temp.append(item[stringfield])
                temp = sorted(temp)
                for a in temp:
                        savedoc.write("%s\n" % a.encode('utf-8'))
                savedoc.close()

        def fieldMapToArray(self, stringfield, collection):
                temp = []
                for item in collection.find():
                        if not any(item[stringfield] in s for s in temp):
                                temp.append(item[stringfield])
                return temp

        #LookUP file specs:
        #file must be coma seperated with parent brand or category as the first element
        #example: if we want the following to be reduced to 'perfumes'
        #a line in the file for the category would look like:
        # perfumes,perfumaria,perfume,feminino

        def buildKeyTable(self, array):
                values = []
                for value in array:
                        for key, value in value.iteritems():
                                values.append(key)
                                values.extend(value)
                return values

        def buildCategoryTable(self, lookupfile):
                catlist = open(lookupfile)
                masterList = []
                for item in catlist.readlines():
                        item = item.split(',')
                        arr = []
                        for a in item:
                                a = a.decode('utf8')
                                a = a.rstrip()
                                arr.append(a)
                        mydic = { arr[0] : arr[1:]}
                        masterList.append(mydic)

                return masterList


class FieldCreator(object):

	def __init__(self):
		self.tables = Tables()

	def makeUnicode(self, string):
		if not isinstance(string, unicode): 
			string = string.encode('utf-8')
			return string
		else:
			return string

	def isEmpty(self, field):
		if len(field) > 0:
			return False
		else:
			return True

	def altMainLoop(self, cat, name):
		
		match = self.nameLoop(name)
		print 'NAME MATCH: %s' % match
		return match

	def mainLoop(self, cat, name):
		match = ''
		if self.isEmpty(cat):
		
			#GOTO NAME SEARCH
			match = self.nameLoop(name)
			print 'Pure Name lookup finds: %s' % match

		else:
			catMatch = self.catLoop(cat)
			if catMatch:
				isValid = self.isValid(catMatch, name)	
				if isValid:
					match = isValid
				else:	
					match = self.nameLoop(name)
						
				# VALIDATE
				#CHEK AGAINST NAME
				#MATCH TO KEY

			else:
				#NO MATRCH CALL NAME LOOP
				match = self.nameLoop(name)
				print 'Post Cat  Name lookup finds: %s' % match
		
		if match:
			
			return match
		else:
			print 'No Match Found :(' 
			return None		

	def isValid(self, dic, name):
		arr = []
		name = self.makeUnicode(name)
		name = name.split() 	
		
		dictionary = deepcopy(dic)
		
		key = dictionary.keys()
		key = key[0]
		value = dictionary[key]
			
		arr.extend(value)
		arr.append(key)

		out = self.dualArrayTokenMatch(arr, name)
				
		print 'VALIDATION ARRAY : %s' % out
		if len(out):
			return  key
		else:
			return None
		## MAKE FINAL VALIDATION HERE
		
		
	def nameLoop(self, name):
		name = self.makeUnicode(name)
		name = name.split()
		matchList = []
		for item in name:
			match = self.matchCatKeyValue(item, self.tables.catTable)
			if match:
				matchList.append(match)
						
		if len(matchList) > 0:
			multiMatchCheck = []
			for item in matchList:
				#match, isKey = self.returnKeyForValue(item, self.tables.catTable)
				key =  item.keys()
				key = key[0]		
				print 'key is: %s' % key 
				multiMatchCheck.append(key)
			if self.isMulti(multiMatchCheck):
				#CASE IF VALUR MATCHES MULTI KEYS RARE BUT SERIOUS
					
				if self.dualCheck(multiMatchCheck):

					return multiMatchCheck[0]
				else:
					return None		
			else:
				return multiMatchCheck[0]		
				# FINISHED RETURNING A SINGLE MATCHED CATEGGORY	
			#check array matches for KEY 
			# DETERMINE BEST ONE IF MULTI
		else:
			print ' NO NAME VALUE OR KEY MATCH PRESENT FOR: %s' % name

			# NO NAME MATCH
	def dualCheck(self, arr):
		b = set(arr)
		if len(b)>1:
			return False	
			print '**** DOUBLE CATEGORY MATCH PROBLEM *****'
		else:
			return True		



	def dualArrayTokenMatch(self, sourceArray, lookupArray):
		out = []
		for word in sourceArray:
			if word in lookupArray:
				out.append(word)
		return out



	def isMulti(self, arr):
		if len(arr)>1:
			return True
		else:
			return False

	def catLoop(self, cat):
		#match Cat to Key 
		#match cat to Value
		#validate
		matchDict = self.matchCatKeyValue(cat, self.tables.catTable)
		if matchDict:
			return matchDict
			# VALIDATE MATCH HERE
		else:
			return None
			#match is none NO MATCH

	def returnKeyForValue(self, value, table):
		for item in table:
			for key, value in item.iteritems():
				if field == key:
					print 'key match returning key : %s ' %key
					#best case the word matches the primary key no more looping through values needed
					return key
				elif field in value:
					print 'value match returning key: %s' % key
					return key
        

	def matchCatKeyValue(self, field, table):
                        match = ''
			for item in table:
				
                                for key, value in item.iteritems():
                                        if field == key:
                                                dic = dict()
						dic = {key:value}
                                                print 'KEY MATCH : %s, %s ' % (dic, field)
						match =  dic
                                        elif field in value:

                                                dic = dict()
						dic = {key:value}
                                                print 'VALUE MATCH: %s, %s' % (dic, field)
                                                match = dic

			return match
	
