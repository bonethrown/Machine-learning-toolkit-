import os,sys,urllib2
import json
import logging
import hashlib
import logging
from nltk import regexp_tokenize, tokenwrap, word_tokenize
import re
import string
logging.basicConfig(filename='matchLog.log', level=logging.DEBUG)
from copy import deepcopy

path = '/home/dev/kk_cosme/cosme/'
brand_path = '/home/dev/kk_cosme/cosme/cosme/pipes/utils/'
INDB = 'production'
INCOLL = 'lalina1018'
OUTDB = 'matching'
OUTCOLL = 'la1018'

TESTDB = 'matching'
TESTCOLL = 'unittest'

class Tables(object):
        def __init__(self):

                self.acc = self.buildCategoryTable(path+'acessorios.list')
                self.cab = self.buildCategoryTable(path+'cabelo.list')
                self.maq = self.buildCategoryTable(path+'maquiagem.list')
                self.hom = self.buildCategoryTable(path+'homem.list')
                self.cor = self.buildCategoryTable(path+'corpo.list')
                self.unh = self.buildCategoryTable(path+'unhas.list')
                self.per = self.buildCategoryTable(path+'perfumes.list')

                #KEY TABLE
                self.catTable = self.buildTree()
                self.brands = self.lineToList(brand_path+'brandric.list')
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

	def lineToList(self, filename):
		List = [line.rstrip() for line in open(filename)]
		return List 

	def arrayToFile(self, name, array):
                savedoc = open(stringfield+'map', 'wb')
		for item in array:
			savedoc.write("%s\n" % item.encode('utf-8'))
	
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
                                a = a.rstrip().lower()
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
