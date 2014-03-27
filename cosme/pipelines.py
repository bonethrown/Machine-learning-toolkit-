# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

##remember to import new added pipes
from scrapy import log
import json, urllib2
from cosme.pipes import pipeMethods
from  pipes.utils import db,utils, itemTools, db2 
import os
from cosme.pipes.belezanaweb import BelezanaWeb
from cosme.pipes.sephora import SephoraSite
from cosme.pipes.magazineluiza import MagazineLuizaSite
from cosme.pipes.infinitabeleza import InfiniteBeleza
from cosme.pipes.default import AbstractSite
from cosme.pipes.sepha import SephaWeb
from cosme.pipes.laffayette import laffayetteWeb
from cosme.pipes.americana import Americanas
from cosme.pipes.submarino import Submarino
from cosme.pipes.walmart import Walmart
from cosme.pipes.dafiti import Dafiti
from cosme.pipes.netfarma import Netfarma
from cosme.pipes import splitPipe
from cosme import dataOps
from cosme.dataOps import nameGen
#simple pipeline for now. Drop Items with no description!

#commitSolr = False
COMMIT_DB = True
SAVE_IMAGE = False
UPDATE_REMOTE = False
MONGO_MIRROR1_HOST = '23.96.17.252'
MONGO_DB_HOST_PORT = 7075

class CosmePipeline(object):
    def __init__(self):
        self.solr_url = "http://localhost:8080/solr/cosme0/update?json"
        #Lets send to ec2 as well
        #self.solr_url_prod = "http://ec2-54-242-158-167.compute-1.amazonaws.com:8080/solr/update?"
        #Set up NonRelDB-Connection
	rawdb = nameGen('raw')
	commentdb = nameGen('rawcomment')
	print 'db for input : %s ' % rawdb
	self.dbManager = dataOps.databaseManager('neworder',rawdb, commentdb)
        self.db = db.getConnection()
        brandsList = os.path.join(os.getcwd(),"cosme","pipes","utils","brandric.list")
        self.matcher = utils.listMatcher(brandsList) 
        self.siteDict = dict()
        self.siteDict['belezanaweb'] = BelezanaWeb()
        self.siteDict['sephora'] = SephoraSite()
        self.siteDict['magazineluiza'] = MagazineLuizaSite()
        self.siteDict['infinitabeleza'] = InfiniteBeleza()
        self.siteDict['default'] = AbstractSite()
        self.siteDict['sepha'] = SephaWeb()
        self.siteDict['laffayette'] = laffayetteWeb()
        self.siteDict['walmart'] = Walmart()
        self.siteDict['submarino'] = Submarino()
        self.siteDict['americanas'] = Americanas()
        self.siteDict['dafiti'] = Dafiti()
        self.siteDict['netfarma'] = Netfarma()
        self.defaultSite = AbstractSite()
	#self.preProcess = preProcess()
    
    def process_item(self, item, spider):
	 #Set this to false if you wish to crawl only and not submit to solr 
        #switch between pipelines , import module accordingly
        pipeModule = "cosme.pipes."+item['site']
        sitePipe = self.siteDict[item['site']]
        
        item = self.defaultSite.process(item, spider)
        #cleanItem = sitePipe.process(item,spider,self.matcher)
  	self.priceProcess(item, sitePipe, spider)
    
    def priceProcess(self, item, sitePipe, spider):
        
	cleanItem = sitePipe.process(item, spider, self.matcher)
  	self.postProcess(cleanItem, spider)
	
	#if item['price'] != 'NA' and itemTools.hasDiffVolume(cleanItem['volume']): 
	#	
	#	if  itemTools.hasDiffPrices(cleanItem):
	#		itemArray = []
	#		itemArray = splitPipe.itemizeByPrice(cleanItem)
	#		print 'Split pipe created : %s items' % itemArray
	#		for cleanItem in itemArray:
	#			finalItem = splitPipe.singularityPipe(cleanItem)
	#			self.postProcess(finalItem, spider)
	#	else:
	#		finalItem = splitPipe.singularityPipe(cleanItem)
#			self.postProcess(finalItem, spider)
#	else:
#		cleanItem = splitPipe.singularityPipe(cleanItem)
  		#self.postProcess(cleanItem, spider)

    def commentCheck(self, item):
	if 'comments' in item:
		#has key 
		return True
	else:
		return False
	
    def postProcess(self, item, spider):
	
	cleanItem = item
	cleanItem['key'] = itemTools.keyGen(item)
	#cleanItem = itemTools.checkVolume(cleanItem)
 
	cleanItem = dict(cleanItem)
        storeItem  = {}
        storeItem['url'] = cleanItem['url']
        storeItem['key'] = cleanItem['key']
	storeItem['site'] = cleanItem['site']
	
	if 'comments' in cleanItem:
        	storeItem['comments'] =  cleanItem['comments']
        	cleanItem['comments'] = []
        if 'name' in cleanItem:
            # No tokenization, but just storing - used for clustering.
            cleanItem['name_noindex']= cleanItem['name']
            
	if COMMIT_DB:
		self.dbManager.updateLalinaItem(cleanItem)
		self.dbManager.updateHistPrice(cleanItem)	
		if 'comments' in storeItem: 
			self.dbManager.updateComment(storeItem)
	if UPDATE_REMOTE:
		self.dbManager.updateRemote(cleanItem)
		self.dbManager.updateRemoteComment(cleanItem)	
	
	if SAVE_IMAGE:
		self.dbManager.saveImageLocally(cleanItem)
	
