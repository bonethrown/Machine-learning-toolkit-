from utils import cleanSymbols
import time
import catChecker
import unicodedata
from utils2 import allToString
import urllib
from nltk import regexp_tokenize, tokenwrap, word_tokenize
import string
from utils import listMatcher
import catChecker
import nltk.classify.util
from nltk import classify
from nltk.classify import NaiveBayesClassifier
import random
from dataOps import databaseManager
import re
from fuzzywuzzy import fuzz
import hashlib
import logging
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz

STOP_BR_PATH = '/home/dev/kk_cosme/cosme/cosme/pipes/utils/stopwords_br.list'
STOP_EN_PATH = '/home/dev/kk_cosme/cosme/cosme/pipes/utils/stopwords_en.list'
SYN_PATH = '/home/dev/kk_cosme/cosme/cosme/pipes/utils/synoynms_en.list'
BRAND_SYN = '/home/dev/kk_cosme/cosme/cosme/pipes/utils/brandmaptable.list'
CATEGORY_LIST = ['perfume', 'unha', 'corpo e banho', 'acessorios', 'homem', 'maquiagem', 'cabelo']

class Dataclean(object):
	
	def __init__(self, db, incoll, outcoll, to_external_db = True):
                self.mem = []
		self.text = TextClean()
		self._filters = WordFilters()
		#self.pc = PriceVolume()
		self.tie = TypeOperations()
		self.indb = databaseManager(db, incoll, incoll)
		self.isExternal = to_external_db	
		if to_external_db:
			
			self.outdb = databaseManager(db, outcoll, outcoll)
			print 'dataclean external db: %s' % self.outdb.getCollection()
		#self.outdb = databaseManager(db, outcoll, outcoll)
		#print self.outdb.getCollection()
	
######NAMAE AND TEXT CLEANING HERE
	def test(self, name):
		name = self._filters.run_filters(name)	
		


	def unitTest(self):
		coll = self.indb.getCollection()
		#function = self.text.removeAllSpaces
		field1 = 'price'
		field2 = 'vol'	
		for count, item in enumerate(coll.find()):
			self.genericBatch(function, item, field1,field2)
			a = item[field1]	
			print a[0]

	def run(self):
		
		coll = self.indb.getCollection()
		print 'Items to clean: %s' % coll.count()
		for count, item in enumerate(coll.find(timeout = False)):

				self.genericBatch(self.text.removeAllSpaces, item, 'price','vol')
				item['name'] = self._filters.run_filters(item['name'])	
				item['name_noindex'] = self.text.cleaner(item['name_noindex'])
				item['category'] = ''
			
				self.tie.run(item)
				del item['_id']
				self.addFields(item)	
				self.write(item)
				self.mem.append(item['key'])

		print 'items cleaned: %s' % self.outdb.getCollection().count()
		print 'errors :%s ' % len(self.mem)
		self.mem = []
	def write(self, item):
		#if self.isExternal:
		#	print item
			self.outdb.updateLalinaItem(item)
		#else:
		#	self.indb.updateLalinaItem(item)
	
	def genericBatch(self, _function, item, prim_field, field):
		if isinstance(item[prim_field], list):
			for value in item[prim_field]:
				out =_function(value[field])
				value[field] = out 
	
	def addFields(self, item):
		try:
			#if not 'price_str' in item:
			#	item['price_str'] = self.pc.floatPriceToString(item['price'])
			if not 'name_url' in item:
				item['name_url'] = self.urlquote(item['name'])
			if not 'ismatched' in item:
				item['is_matched'] = 0
			#if '_id' in item:
			#	print 'removed' 
			#	del item['_id']
			
		except Exception, e:
			print 'field add exception : %s , %s' % (e,item)
	
	def urlquote(self, string):
                string = unicodedata.normalize('NFKD', string).encode('ascii','ignore')
                string = string.replace(" ","-")
                string = urllib.quote(string)
                return string


class WordFilters(object):
	def __init__(self):
		#matcher removes the brand
		self.text = TextClean()
		self.matcher = listMatcher()
		self.cat_list= CATEGORY_LIST
		self.syn = catChecker.Tables.buildCategoryTable(SYN_PATH)
		self.stop_br = catChecker.Tables.commaFileToList(STOP_BR_PATH)
		self.stop_en = catChecker.Tables.commaFileToList(STOP_EN_PATH)
		self.stop_en.extend(self.stop_br)
		self.stop_en = set(self.stop_en)
		self.brand_syn = catChecker.Tables.buildCategoryTable(BRAND_SYN)	
		self.cat = CATEGORY_LIST
	
        def stopfilter(self, name, filter_list):
                name = name.split()
                filtered = [k for k in name if not k in filter_list]
                out =" ".join(filtered)
                return out

	def run_filters(self, out):
		#out = fuzz.asciidammit(out)
		#start =time.time()
		#initial cleaning
		out = self.text.cleaner(out)
		#print '1. ' + out
		#remove stop words
		out = self.stopfilter(out, self.stop_en)
		#print '2. ' + oui
		#expand synonyms
		out = self.syn_map(out, self.syn)
		# remove brands
		out = self.syn_map(out, self.brand_syn)
		#print '4. ' + out
		out = self.dupRemove(out)

		out = self.stopfilter(out, self.cat)
		
		out = self.matcher.removeMatch(out)	
		#print '5. ' + out
		out = self.text.removeMidWhiteSpaces(out)
		
		out = out.strip()
		#print 'elapsed time: %s' % (end-start)
		return out	

	def syn_map(self, name, table):
		for item in table:
			for key, value in item.iteritems():
				for word in value:
					re_find = re.search(word, name)
					if re_find:
						re_found = re_find.group()
						name = name.replace(re_found, key)
		return name

	def dupRemove(self, a):
		a = ' '.join(self.unique_list(a.split()))
		return a

	def unique_list(self, l):
		ulist = []
		[ulist.append(x) for x in l if x not in ulist]
		return ulist


class TextClean(object):
	def __init__(self):
                self.pc = PriceVolume()
		#self.matcher = listMatcher()
		self.pattern = r'(?x)\n  ([A-Z]\\.)+  \n | \\w+(-\\w+)*\n| \\$?\\d+(\\.\\d+)?%?\n| \\.\\.\\.\n| [][.,;"\'?():-_`]\n'
                
		self.volPattern = r'''(?i) \d+ml|\d+ ml|\d+ML|\d+ML|\d+g|\d+ g|\d+gr|\d+ gramas|\d+ gr|\d+gramas'''	
	def cleaner(self, newName, remove_brand = True):
		#ORDER IMPORTTAN
		#if not isinstance(newName, unicode):
		#	newName = newName.decode('utf8')
		newName = newName.lower()
		#newName = self.quickExpand(newName)
		#newName = self.punctuationStripper(newName)
		#newName = self.cleanName(newName)
		newName = cleanSymbols(newName)	
		newName = self.pc.cleanVolume(newName)
		newName= self.clean_numbers(newName)	
		#newName = self.dupRemove(newName)
		#newName = self.removeMidWhiteSpaces(newName)
		#newName = newName.strip()
		return newName

	@staticmethod
	def url_2_name(url):
		url = url.split('/')
		url = url[-1]
		url = url.replace('-',' ')
		return url

	def clean_numbers(self, name):
		keep = ['212','2012','2013','2014']
		name = name.split()
		for word in name:
			if word.isdigit() and word not in keep:
				name.remove(word)
		return " ".join(name)

	
	def removeMidWhiteSpaces(self, name):
                name = re.sub(r'\s+', ' ', name)
                return name

	def punctuationStripper(self, string):
                start = time.time()
		phrase = string.strip()
                phrase = phrase.split(' ')
                out = []
                for item in phrase:
                        a = ''.join(e for e in item if e.isalnum())
                        out.append(a)
                out = ' '.join(out)
                end = time.time()
                print ' run time: %s' % (end-start)
		return out

	def cleanName(self, name):
                start = time.time()
                exclude = set(string.punctuation)
                out = ''.join(ch for ch in name if ch not in exclude)
                end = time.time()
                print ' run time: %s' % (end-start)

                return out

	def quickExpand(self, name):
		r = r'edt|edp|c/|p/|eau de parfum|homme'
		expanddict = { 'p/':'para','c/':'com','edt' : 'eau de toilette', 'edp': 'eau de perfume','eau de parfum':'eau de perfume','homme':'masculino','edc':'eau de cologne' }
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

	def removeAllSpaces(self, string):
		return "".join(string.split()).lower()
	
class TypeOperations(object):
	def __init__(self):
	
		self.no_op= ['price']	

	def run(self, item):
		for key, value in item.iteritems():
			if key not in self.no_op:
				item[key] = allToString(item[key])

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

class PriceVolume(object):

	def __init__(self):
		self.volPattern = r'''(?i) \d+ml|\d+ ml|\d+ML|\d+ML|\d+g|\d+ g|\d+gr|\d+ gramas|\d+ gr|\d+gramas'''		
	def clean_vol(self, volume):
		out = self.cleanSingleVolume(volume)
		out = self.removeAllSpaces(volume)
		return out 

	def checkPrice(self, item):
		price = item['price'][0]
		key = item['key']
		if not item['price'] == 'NA':
			if isinstance(price, float):
				pass
			else:
				print 'Price not Float: %s : key %s' % (price, key)

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
                               	if not isinstance(priceFloat, str) or isinstance(priceFloat, unicode): 
                                	pricestr = '%.2f' % priceFloat
                              		return pricestr
				else:
					return priceFloat
                        else:
                                return priceFloat
	#NOT INTENDED TO USE WITH VOLUME FILED ONLY FOR NAME FIELD CLEANING
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
