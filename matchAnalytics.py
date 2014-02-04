from cosme.dataOps import databaseManager
import pymongo
from operator import itemgetter
class Analytics(object):
	
	def __init__(self, db, coll):
		self.manager = databaseManager(db, coll, coll)

	def getCollection(self):
		print self.manager.getCollection()
		return self.manager.getCollection()

	def fieldValueCount(self, field):
		list_count = 0
		string_count = 0
		float_count = 0
		na_count = 0
			
		for item in self.getCollection().find():
			temp = item[field][0]
			if isinstance(temp, float):
				float_count = float_count +1
			elif temp == 'NA':
				na_count = na_count + 1
			else: 
				string_count = string_count +1
		print 'Float : %s NA : %s OTher: %s ' % (float_count,na_count,string_count)
				 			
	def countfield(self, field):
		list_count = 0
		string_count = 0
		float_count = 0
		uni_count = 0
		total = self.getCollection().count()
		for item in self.getCollection().find():
			if isinstance(item[field], list):
				list_count = list_count +1 
			elif isinstance(item[field], str):
				string_count = string_count +1
			elif isinstance(item[field], float):
				float_count = float_count +1
			elif isinstance(item[field], unicode):
				uni_count = uni_count +1
		print 'List : %s string : %s float: %s unicode: %s total: %s' % (list_count,string_count,float_count,uni_count,total)
				
	def avgScores(self):
		count = 0
		namescore = 0
		partialscore = 0
		tokensetscore = 0
		parent = 0
		child = 0
		mainCount = self.getCollection().count()
		for item in self.getCollection().find():
			if 'matchscore' in item:
				temp = item['matchscore']
				if isinstance(temp, dict):
					count = count +1
					namescore = temp['fuzzratio'] + namescore
					partialscore = temp['partialsort']+ partialscore
					tokensetscore = temp['tokenset'] + tokensetscore

				if 'rank' in item:
					parent = parent + 1
				else:
					child = child + 1

		nameAvg = float(namescore) / float(count)
		partialAvg = float(partialscore) / float(count)
		tokenAvg = float(tokensetscore) / float(count)
		Average = nameAvg + partialAvg + tokenAvg
		avg = float(Average) / 3
		total = parent + child 	
		diff = mainCount - total	
		print 'Items in Collection: %s' % mainCount
		print 'total matched count: %s ' % count
		print 'parents: %s  childs: %s , total : %s , diff: %s' % (parent, child, total, diff)
		print 'Avg fuzzname score: %s, Avg partial : %s, Avg token: %s' % (nameAvg, partialAvg, tokenAvg)
		print 'full average is : %s' % avg

	#count how many distinct field values there are:
	#USe only for fields that can take a finite number of vlalues, liek Site, category
	def fieldCount(self, field):
		coll = self.getCollection()
		sites = coll.distinct(field)
		out = []
		for item in sites:
			count = coll.find({field: item}).count()
			tup = (item, count) 
			out.append(tup)
	
		return out
			
	# TOBE USED TO CHEK SUM of brands vs database count with output of fieldCount
	def checkSum(self,arrOfTupples):
		coll = self.getCollection()
		count = coll.count()
		total = 0
		for item in arrOfTupples:
			total = item[1] + total
		
		return "Total : %s Count : %s " % (total, count)

	def alphabetical(self, data):	
		return sorted(data, key = itemgetter(0))

	def avgMatchCount(self, arrOfTupples):
		total = 0
		count = len(arrOfTupples)
		for item in arrOfTupples:
			total = item[1] + total
		
		avg = float(total) / float(count)
		return 'Average no of matcher per item: %s' % avg
	#use with output of fieldCount moethod
	def getBottomCount(self, lessThan, arrOfTupples):
		arr = self.top10(arrOfTupples)
		bottom = []
		for tup in arr:
			if tup[1] < lessThan:
				bottom.append(tup[0])
		return bottom
	def top10(self, data):
		return sorted(data, key = itemgetter(1))

	def nameQuality(self):
		coll = self.getCollection()
		count = 0
		unique = 0
		arr = []
		sites = coll.distinct('site')
		for site in sites:
			site_count = coll.find({'site':site}).count()
			for item in coll.find({'site': site}):
				name = item['name'].split()
				count = len(name)+ count
				unique = len(set(name))+ unique
				
			site_avg = float(count) / float(site_count)
			site_unq = float(unique) / float(site_count)

			out = (site, site_avg, site_unq)
			arr.append(out)
			count = 0
			unique = 0
							
		print '(site, average words count, unique words)'
		return arr							 
	

	
