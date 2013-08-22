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
INCOLL = 'mapthree'	
OUTDB = 'matching'
OUTCOLL = 'maptest'

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
	
	def makeMappingCopy(self):
		for item in self.indb.find():
			if 'name' in item:
				pass
			else: 
				print item['key']
			if 'name' in item:
				try:
					copyObject = item 
					newName = self.cleaner(item['name'])
					newVolume = self.remVolWhiteSpace(item['volume'])
					
					copyObject['volume'] = newVolume
					copyObject['name'] = newName
					copyObject['key'] = item['key']
					print 'name OUT: ' + copyObject['name']+' Name in : ' +item['name']
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
		matchVolumized(db)

#if __name__ == "__main__":

    #first argument: batch size
    #second argument: dmp or feed
    #third argument : filename
    
