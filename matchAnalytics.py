from cosme.dataOps import databaseManager


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
		for item in self.getCollection().find():
			if 'matchscore' in item:
				temp = item['matchscore']
				if isinstance(temp,dict):
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
		print 'total matched count: %s ' % count
		print 'parents: %s  childs: %s , total : %s' % (parent, child, total)
		print 'Avg fuzzname score: %s, Avg partial : %s, Avg token: %s' % (nameAvg, partialAvg, tokenAvg)
		print 'full average is : %s' % avg
		
