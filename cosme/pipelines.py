# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

##remember to import new added pipes
from scrapy import log
import json, urllib2
from cosme.pipes import pipeMethods
from  pipes.utils import db,utils, itemTools
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

COMMENT_DB = 'itemTest'
PROD_DB = 'lalina'
TEST_DB = 'testLalina'
#commitSolr = False
commitDB = True	
prodDB = True	
SAVE_IMAGE = True

class CosmePipeline(object):
    def __init__(self):
        self.solr_url = "http://localhost:8080/solr/cosme0/update?json"
        #Lets send to ec2 as well
        #self.solr_url_prod = "http://ec2-54-242-158-167.compute-1.amazonaws.com:8080/solr/update?"
        #Set up NonRelDB-Connection
	self.dbManager = dataOps.databaseManager()
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
			#print "**************HAS MULTI DIFF PRICE"
			#print cleanItem
			itemArray = []
			itemArray = splitPipe.itemizeByPrice(cleanItem)
			print itemArray
			for cleanItem in itemArray:
				finalItem = splitPipe.singularityPipe(cleanItem)
				self.postProcess(finalItem, spider)
		else:
			print " multi price but not DIFFERENT ************************"
			finalItem = splitPipe.singularityPipe(cleanItem)
			self.postProcess(finalItem, spider)
	else:
		print "*********** non multi price*************"
		print cleanItem['volume']
		print cleanItem
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
        #print singleItemJson
        #log.msg("Getting ready to send %s "%singleItemJson, level=log.DEBUG)

        #if commitSolr:
         #   try:
          #      req  = urllib2.Request(self.solr_url, data = singleItemJson)
           #     req.add_header("Content-type", "application/json")
           # except Exception, e:
            #    log.msg("************* ERROR Submitting to mongoDB error: %s "%e, level=log.ERROR)
            
	if commitDB:
		self.dbManager.updateLalinaItem(cleanItem)
		self.dbManager.updateComment(storeItem)
		self.dbManager.updateHistPrice(cleanItem)	
	if SAVE_IMAGE:
		self.dbManager.saveImageLocally(cleanItem)
	
#    try	self.:
         #       print " ****************************************************SENDING TO DB"
	#	# SUBMIT TO DB ONLY IF RESPONSE FROM SOLR
         #       if storeItem['comments']:
	#		self.db.itemsTest.update({"key" : storeItem['key']},{"comments" : storeItem['comments'], "url" : storeItem['url'], "key" : storeItem['key'], "site" : storeItem['site']}, upsert=True)
         #       if prodDB:
	#		self.dbManager
	#		self.db.lalina.update({"key" : cleanItem['key']}, cleanItem, upsert=True)
         #       	log.msg("********* MONGO SUBMITTED ****** with response", level=log.DEBUG)
            		#self.dbManager.updateSecondaryFields(cleanItem)

	#	else:
			#updateParams = { "$set" : { 'price' : cleanItem['price']}, "$set" : { 'volume' : cleanItem['volume']} }
	#		self.db.testLalina.update({"key" : cleanItem['key']}, cleanItem, upsert=True)
	#		log.msg('updated item %s' % cleanItem['key'])
	 #   except Exception, e:
                #og.msg("***********ERROR Submitting to MONGO error: %s"%e, level=log.ERROR)
       # else:
        #    log.msg("*********** Not commiting to solr or DB commit set to false  ",level=log.WARNING)

       # return cleanItem	 
