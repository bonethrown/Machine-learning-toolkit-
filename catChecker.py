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
        
	def commaFileToList(self, lookupfile):
                catlist = open(lookupfile)
                masterList = []
                for item in catlist.readlines():
                        item = item.split(',')
                        arr = []
                        for a in item:
                                a = a.decode('utf8')
                                a = a.rstrip()
                                arr.append(a)
                        masterList.extend(arr)
		return masterList



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

        
