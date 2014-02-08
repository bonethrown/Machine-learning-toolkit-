from cosme.dataOps import databaseManager
import pymongo
from random import shuffle
from mapperSet import BayesObject, Name
CATEGORY_LIST = ['perfume', 'unha', 'corpo e banho', 'acessorios', 'homem', 'maquiagem', 'cabelo']
from nltk import FreqDist
import math

class Benchmark(object):

	def __init__(self, db, coll):
		self.manager = databaseManager(db, coll, coll)
		self.rand_list = self.randomExtract()
		self.bayes = BayesObject()
		self.bayes.initdatabase(db, coll)
	
		#data sets
		self.test_set, self.dev_set, self.train_set = self.createDataSets()
		
		print self.manager.getCollection()
	def getCollection(self):
		return self.manager.getCollection()
	# extract random amount from unmatched category
	#int num is total items to extract i
	def featurizeName(self):
		
		out = []
		for item in arr:
			if isinstance(item, Name):
				features = item.customFeaturize(item.name)
				out.append(features)
		return out
	def setCat(self, arr):
		for item in arr:
			itemm['category'] = ''

	def entropy(labels):
		freqdist = FreqDist(labels)
    		probs = [freqdist.freq(l) for l in nltk.FreqDist(labels)]
    		return -sum([p * math.log(p,2) for p in probs])

	def createDataSets(self):
		main = self.bayes.loadCorpus(self.devTestSet(1000))
		shuffle(main)
		test_set = main[:500]
		dev_set =main[500:]
		
		training_set = dev_set[:250]
		dev = dev_set[250:]
		return test_set,dev, training_set
	def devTestSet(self,number=1000):
		out = []
		grab = float(number) / float(len(CATEGORY_LIST))
		grab = int(round(grab,0))
		for cat in CATEGORY_LIST:
			out.extend(self.matchedSample(cat,grab))
		return out

	def matchedSample(self, category, number):
	 	arr =  list(self.getCollection().find({'category' : category}).limit(number))
		return arr
		
	def randomExtract(self, amount=100):
	 	arr =  list(self.getCollection().find({'category' : ''}))
		shuffle(arr)
		extract = arr[:amount]
