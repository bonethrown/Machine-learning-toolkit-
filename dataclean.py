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

class Dataclean(object):
	
	def __init__(self, db, incoll):
                self.mem = []
		self.text = TextClean()
		self.pc = PriceVolume()
		self.tie = TypeOperations()
		self.indb = databaseManager(db, incoll, incoll)
		#self.outdb = databaseManager(db, outcoll, outcoll)
		print self.indb.getCollection()
		#print self.outdb.getCollection()
	
######NAMAE AND TEXT CLEANING HERE
	def run(self, with_Brand=False):
		
		coll = self.indb.getCollection()
		for count, item in enumerate(coll.find(timeout = False)):

			try : 
				item['name'] = self.text.cleaner(item['name'], with_Brand)	
				item['volume'] = self.text.removeAllSpaces(item['volume'])
				item['category'] = ''
				self.tie.run(item)
				eelf.addFields(item)
				self.indb.updateLalinaItem(item)
			except Exception, e:
				self.mem.append(e, item['key'])
		self.mem = []

	def addFields(self, item):
		if not 'price_str' in item:
			item['price_str'] = self.pc.floatPriceToString(item['price'])
		if not 'name_url' in item:
			item['name_url'] = self.urlquote(item['name'])
		if not 'ismatched' in item:
			item['is_matched'] = 0
			
	def urlquote(self, string):
                string = unicodedata.normalize('NFKD', string).encode('ascii','ignore')
                string = string.replace(" ","-")
                string = urllib.quote(string)
                return string

class TextClean(object):
	def __init__(self):
                self.pc = PriceVolume()
		self.matcher = listMatcher()
		self.pattern = r'(?x)\n  ([A-Z]\\.)+  \n | \\w+(-\\w+)*\n| \\$?\\d+(\\.\\d+)?%?\n| \\.\\.\\.\n| [][.,;"\'?():-_`]\n'
                self.volPattern = r'''(?i) \d+ml|\d+ ml|\d+ML|\d+ML|\d+g|\d+ g|\d+gr|\d+ gramas|\d+ gr|\d+gramas'''	
	def cleaner(self, newName, remove_brand = True):
		#ORDER IMPORTTAN
		if not isinstance(newName, unicode):
			newName = newName.decode('utf8')
		newName = newName.lower()
		newName = self.quickExpand(newName)
		newName = self.punctuationStripper(newName)
		newName = self.cleanName(newName)
		newName = self.pc.cleanVolume(newName)
		newName = self.dupRemove(newName)
		newName = self.removeMidWhiteSpaces(newName)
		if remove_brand:
			newName = self.matcher.removeMatch(newName)
		newName = self.removeMidWhiteSpaces(newName)
		newName = newName.strip()
		return newName

		
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

	def removeAllSpaces(self, string):
		return "".join(string.split()).lower()
	
class TypeOperations(object):
	
	def run(self, item):
		for key, value in item.iteritems():
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
