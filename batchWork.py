# READ ME 
#
#
#################
# ALL BATCH CODE REQURED A dataOps. databasemanager object passed to them 
###############
import urllib
import unicodedata
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

class Batchwork(object):
	def __init__(self, db, coll):
		self.manager = databaseManager(db,coll)
	

	def genericBatch(self, _function,field1, field2):
		coll = self.manager.getCollection()
		for item in coll.find():
			mod = item[field1]
			out =_function(mod)
			item[field2] = out
			self.manager.updateLalinaItem(item)
			

	def urlquote(self, string):
		string = unicodedata.normalize('NFKD', string).encode('ascii','ignore')
		string = string.replace(" ","-")
		string = urllib.quote(string)
		return string

	def runBatch(self):
		self.batchNullFix(self.manager, 'price_per_vol')
		self.batchNullFix(self.manager, 'price_str')
		self.batchNoToUni('price_per_vol')
		self.batch
	def batchNoToUni(self, field):
		coll = self.manager.getCollection()
		count = coll.count()
		print count
		for item in coll.find():
			self.numberToString(item,field)				

	def numberToString(self, item, field):
			if isinstance(item[field], float):
				out = str(item[field])
				item[field] = out
				self.manager.updateLalinaItem(item)
			elif isinstance(item[field], int):
				out = str(item[field])
				item[field] = out
				self.manager.updateLalinaItem(item)
			else:
				pass

	def batchCleanVolume(self):
		coll = self.manager.getCollection()
		for item in coll.find():
			if item['volume'] is None:
				item['volume'] = 'NA'
			if item['volume'] == '':
				item['volume'] = 'NA'
			elif len(item['volume']) == 0:
				item['volume'] = 'NA'
			elif item['volume'] == ['NA']:
				item['volume'] = 'NA'
			self.manager.updateLalinaItem(item)

	def batchNullFix(self, manager, field):
		coll = manager.getCollection()
		count = coll.find( { field: None }).count()
		print count
		value = None
		manager.updateByField(field, value, 'na')
		count = coll.find( { field: None }).count()
		print count

	def stampDummyKey(self,manager):
        #this is needed for solr to group things by groupid.
		outdb = manager.getCollection()
                counter = 0
                toPatch = outdb.find({ 'groupid': { '$exists': 0}}).count()
                for item in outdb.find({ 'groupid': { '$exists': 0}}):
                        if not 'groupid' in item:
                                item['groupid'] =self.dummyGroupKey(item)
                                manager.updateLalinaItem(item)
                                counter = counter+ 1
                print 'items patched: %s ' % counter
                print 'items needed patching %s ' %toPatch

	def dummyGroupKey(self, item):
                if not 'groupid' in item:
                        groupid = '0000' + item['key']
                        return groupid
                else:
                        return item['groupid']

	def desArrString(self, field):
		if isinstance(field, list):
			if field:
				for item in field:
					out = " ".join(item)
					return out
			else: 
				return 'na'
		else:
			return None

    	def arrayToString(self, field):
		if isinstance(field, list):
			if field:
					field = field[0]
					out = "".join(field)
					return out
			else: 
				return 'na'
		else:
			return None
	def batchDesToString(self, manager, field):
		coll = manager.getCollection()
		count = 0
		for item in coll.find():
			value = item[field]
			value = self.desArrToString(value)
			if value:
				count = count + 1
				item[field] = value
				manager.updateLalinaItem(item)
			
		print 'fixed : %s' % count
	def batchArrayToString(self, manager, field):
		coll = manager.getCollection()
		count = 0
		for item in coll.find():
			value = item[field]
			value = self.arrayToString(value)
			if value:
				count = count + 1
				item[field] = value
				manager.updateLalinaItem(item)
			
		print 'fixed : %s' % count
