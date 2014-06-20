from dataOps import databaseManager
import os

import string
import time

import xml.sax.saxutils

#
# Document extentions we are interested in generating data for.
#

DOMAIN = "http://www.lalina.com.br/"
S = "/"
# The default default is "Never"
class Sitemap(object):

	def __init__(self, db='neworder', coll='jan_proctwo'):
		self.manager = databaseManager(db, coll)
		print self.manager
	def arrayToFile(self, name, array):
		savedoc = open(name, 'wb')
		for item in array:
			savedoc.write("%s\n" % item.encode('utf-8'))

	def batch_to_file(self):
		coll = self.manager.getCollection()
		savedoc = open('sitemap.txt', 'wb')
		
		for doc in coll.find():
			url = DOMAIN+doc['category']+S+doc['brand']+S+doc['url_name']+S+doc['key']
			savedoc.write("%s\n" % url.encode('utf-8'))
