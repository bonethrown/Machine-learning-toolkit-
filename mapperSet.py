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

INDB = 'matching'
INCOLL = 'maptest'	
OUTDB = 'matching'
OUTCOLL = 'sep112013'

class Mapreduce(object):

	def __init__(self):
		self.pattern = r'(?x)\n  ([A-Z]\\.)+  \n | \\w+(-\\w+)*\n| \\$?\\d+(\\.\\d+)?%?\n| \\.\\.\\.\n| [][.,;"\'?():-_`]\n'

		self.volPattern = r'''(?i) \d+ml|\d+ ml|\d+ML|\d+ML|\d+g|\d+ g|\d+gr|\d+ gramas|\d+ gr|\d+gramas'''

		self.connection = Connection()

		self.indb = self.connection[INDB]
		self.indb = self.indb[INCOLL]

		outdb = Connection()
		outdb = outdb[OUTDB]
		self.outdb = outdb[OUTCOLL]
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

	def removeMidWhiteSpaces(self, name):
		name = re.sub(r'\s+', ' ', name)
		return name	
	
		
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
	
	def cleaner(self, newName):
		#ORDER IMPORTTAN
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

	def makeMappingCopy(self):
		for item in self.indb.find():
			if 'name' in item:
				try:
					copyObject = item 
					newName = self.cleaner(item['name'])
					newVolume = self.remVolWhiteSpace(item['volume'])
					self.lowerfields(copyObject) 
					copyObject['price_str'] = self.floatPriceToString(item['price'])		
					copyObject['volume'] = newVolume
					copyObject['name'] = newName
					copyObject['key'] = item['key']
					copyObject['groupid'] = self.dummyGroupKey(item)
					self.updateInDb(copyObject)	
					#self.mem.append(copyObject)
				except Exception, e:
					print e
					self.mem.append(item['key'])
					
					print item['key']	
		#self.updateInDb(self.mem.append)
		print ' error : %s ' % len(self.mem)
		print 'coppied %s' % self.outdb.count()

	 
	def updateInDb(self, item):
		try:
			self.outdb.insert(item, safe=True)
		
		except Exception, e:
			print 'mongo exception'

		
	def main(collection):
		connection = Connection()
		db = connection[OUTDB]
		db = db[collection]
		print 'collection in use %s' %db
		
#if __name__ == "__main__":

    #first argument: batch size
    #second argument: dmp or feed
    #third argument : filename
    
