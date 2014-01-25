from cosme.dataOps import databaseManager
import pymongo

class Analytics(object):
	
	def __init__(self, db, coll):
		self.manager = databaseManager(db, coll, coll)

	def getCollection(self):
		print self.manager
		return self.manager.getCollection()
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

	def siteCount(self):
		coll = self.getCollection()
		sites = coll.distinct('site')
		out = []
		for item in sites:
			count = coll.find({'site': item}).count()
			site_count = item + " : " + str(count)
			out.append(site_count)
		return out		
