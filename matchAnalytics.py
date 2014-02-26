from cosme.dataOps import databaseManager
import pymongo
from operator import itemgetter

MATCH_ORDER = [ {'belezanaweb':0}, {'sepha':0}, {'sephora':0}, {'magazineluiza':0}, {'laffayette':0}, {'dafiti':0}, {'infinitabeleza':0}, {'americanas':0}, {'submarino':0}, {'walmart':0}, {'netfarma':0} ]
class Analytics(object):
	
	def __init__(self, db, coll):
		self.manager = databaseManager(db, coll, coll)

	def getCollection(self):
		return self.manager.getCollection()


	def match_distribution(self):
		beleza = 0
		sepha = 0
		sephora =0
		magazine = 0
		laffayette = 0
		dafiti = 0
		infinita = 0
		americanas = 0
		submarino = 0
		walmart = 0
		netfarma = 0

		coll = self.getCollection()
		print coll.count()
		for item in coll.find():	
			for ele in item['sites']:
				obj = ele['site']
				if obj == 'belezanaweb':
					beleza = beleza + 1
				if obj == 'sepha':	
					sepha = sepha + 1
				if obj == 'sephora':
					sephora = sephora +1
				if obj == 'magazineluiza':
					magazine = magazine +1
				if obj == 'laffayette':
					laffayette = laffayette +1
				if obj == 'dafiti':
					dafiti = dafiti + 1
				if obj == 'infinitabeleza':
					infinita = infinita + 1
				if obj == 'americanas':
					americanas = americanas + 1
				if obj == 'walmart':
					walmart = walmart + 1
				if obj == 'submarino':
					submarino = submarino + 1
				if obj == 'netfarma':
					netfarma = netfarma + 1
		print "beleza: %s sepha: %s sephora: %s magazine: %s laff: %s dafiti: %s infinita: %s americanas: %s walmart: %s submarino: %s netfarma: %s" % (beleza, sepha, sephora, magazine, laffayette, dafiti, infinita, americanas, submarino, walmart, netfarma)

	def matchCount(self):
		coll = self.getCollection()
		zero = 0
		one = 0
		two = 0
		three = 0
		four = 0
		five = 0
		six_plus = 0
		total = coll.count()
		for item in coll.find():
			matches = len(item['sites'])
			if matches == 1:
				zero = zero + 1
			if matches == 2:
				one = one + 1
			if matches == 3:
				two = two + 1
			if matches == 4:
				three = three + 1
			if matches ==5:
				four = four + 1
			if matches == 6:
				five = five + 1
			if matches >= 7:
				six_plus = six_plus + 1

		matched = one + two + three + four + five + six_plus
		print "0: %s, 1: %s, 2: %s, 3: %s, 4: %s, 5: %s, 6+: %s matched: %s" % (float(zero)/total, float(one)/total, float(two)/total, float(three)/total, float(four)/total, float(five)/total, float(six_plus)/total, float(matched)/total)  	
		return "0: %s, 1: %s, 2: %s, 3: %s, 4: %s, 5: %s, 6+: %s matched: %s total: %s" % (zero, one, two, three, four, five, six_plus, matched, total)  	
		


	def allFieldsType(self):
		coll = self.getCollection()
		sample = list(coll.find().limit(1))
		sample = sample[0]
		keys = sample.keys()
		keys.remove('_id')
		out = []
		print 'keys: %s' % keys
		for key in keys:
			response = self.countType(key)
			print response
			out.append((key, response))
		return out
	
	def countType(self, field):
		list_count = 0
		string_count = 0
		float_count = 0
		uni_count = 0
		int_count =0 
		_None = 0
		no_field = 0
		total = self.getCollection().count()
		for item in self.getCollection().find():
			
			if field in item:
				if  isinstance(item[field], list):
					list_count = list_count +1 
				elif isinstance(item[field], int):
					int_count = int_count +1
				elif isinstance(item[field], str):
					string_count = string_count +1
				elif isinstance(item[field], float):
					float_count = float_count +1
				elif isinstance(item[field], unicode):
					uni_count = uni_count +1
				elif isinstance(item[field], None):
					_None = _None + 1
			else:
				no_field = 1 + no_field

		out = 'Int: %s List: %s string: %s float: %s unicode: %s None: %s NoField: %s total: %s' % (int_count,list_count,string_count,float_count,uni_count, _None, no_field, total)
		return out		
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

	
	#use with new object class newLalinaitem
	#def newMatchCount(self):	
		

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
