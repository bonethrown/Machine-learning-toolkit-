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
from cosme.pipes import splitPipe
from cosme import dataOps
#simple pipeline for now. Drop Items with no description!

#commitSolr = False
COMMIT_DB = False
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
	self.dbManager = dataOps.databaseManager('neworder','sephasitebot')
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

	if item['price'] != 'NA' and itemTools.hasMultiPrice(cleanItem): 
	
		if  itemTools.hasDiffPrices(cleanItem) and not item['site'] == 'sepha':
			print "**************ITEMIZE BY PRICE **************"
			#print cleanItem
			itemArray = []
			itemArray = splitPipe.itemizeByPrice(cleanItem)
			print itemArray
			for cleanItem in itemArray:
				finalItem = splitPipe.singularityPipe(cleanItem)
				self.postProcess(finalItem, spider)
		else:
			print " Non different multi price singularity pipe ************************"
			finalItem = splitPipe.singularityPipe(cleanItem)
			self.postProcess(finalItem, spider)
	else:
		print "*********** Pipeline Singularity Pipe*************"
		print cleanItem['volume']
		cleanItem = splitPipe.singularityPipe(cleanItem)
		self.postProcess(cleanItem, spider)
	
    def postProcess(self, item, spider):
	
	cleanItem = item
	cleanItem['key'] = itemTools.keyGen(item)
	#cleanItem = itemTools.checkVolume(cleanItem)
        print " *****CLEAN ITEM ********"
	print cleanItem
 
	cleanItem = dict(cleanItem)
        storeItem  = {}
        storeItem['url'] = cleanItem['url']
        storeItem['comments'] =  cleanItem['comments']
        storeItem['key'] = cleanItem['key']
	storeItem['site'] = cleanItem['site']
        cleanItem['comments'] = []
        if 'name' in cleanItem:
            # No tokenization, but just storing - used for clustering.
            cleanItem['name_noindex']= cleanItem['name']
        arrItem = []
        arrItem.append(dict(cleanItem))
        #log.msg("Item ready for json %s "%arrItem, level=log.DEBUG)
        singleItemJson = json.dumps(arrItem)
            
	if COMMIT_DB:
		self.dbManager.updateLalinaItem(cleanItem)
		self.dbManager.updateComment(storeItem)
		self.dbManager.updateHistPrice(cleanItem)	
	if UPDATE_REMOTE:
		self.dbManager.updateRemote(cleanItem)
		self.dbManager.updateRemoteComment(cleanItem)	
	
	if SAVE_IMAGE:
		self.dbManager.saveImageLocally(cleanItem)
	
