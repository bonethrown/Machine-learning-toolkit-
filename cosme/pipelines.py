# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

##remember to import new added pipes
from scrapy import log
import json, urllib2
from  pipes.utils import db,utils
import os
from cosme.pipes.belezanaweb import BelezanaWeb
from cosme.pipes.sephora import SephoraSite
from cosme.pipes.magazineluiza import MagazineLuizaSite
from cosme.pipes.infinitabeleza import InfiniteBeleza
from cosme.pipes.default import AbstractSite
from cosme.pipes.sepha import SephaWeb
from cosme.pipes.laffayette import laffayetteWeb


#simple pipeline for now. Drop Items with no description!
class CosmePipeline(object):
    def __init__(self):
        self.solr_url = "http://localhost:8080/solr/cosme0/update?json"
        #Lets send to ec2 as well
        self.solr_url_prod = "http://ec2-54-242-158-167.compute-1.amazonaws.com:8080/solr/update?"
        #Set up NonRelDB-Connection
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

       
    def process_item(self, item, spider):
        #Set this to false if you wish to crawl only and not submit to solr 
        commit = True
        #switch between pipelines , import module accordingly
        pipeModule = "cosme.pipes."+item['site']
        log.msg("Opening Module %s for parsing"%pipeModule, level=log.INFO)
        
        sitePipe = self.siteDict[item['site']]
        
        #Parse with default pipeline first to handle generic stuff.
        #parse item with custom pipeline
        #print "Parsing item %s",(item)
        item = self.defaultSite.process(item, spider)
        cleanItem = sitePipe.process(item,spider,self.matcher)
	if cleanItem['volume'] == None:
		cleanItem['volume'] = ""
        cleanItem['key'] = utils.createKey(cleanItem)
	clean = dict(cleanItem)
	
	storeItem  = {}
	storeItem['url'] = cleanItem['url']
        storeItem['comments'] =  cleanItem['comments']
        storeItem['key'] = clean['key'] 
	cleanItem['comments'] = []
        arrItem = []
        arrItem.append(dict(cleanItem))

        
        #log.msg("Item ready for json %s "%arrItem, level=log.DEBUG)
        singleItemJson = json.dumps(arrItem)
        #print singleItemJson 
        #log.msg("Getting ready to send %s "%singleItemJson, level=log.DEBUG)

        if commit:
            try:
                req  = urllib2.Request(self.solr_url, data = singleItemJson)
                req.add_header("Content-type", "application/json")
                #send data to MongoDB vids collection (sample use nubunu_db; db.vids.find();)
                # resultDB = self.db.items.insert(dict(storeItem),safe=True )
                #resultDB_raw = self.db.vids_raw.insert(dict(storeItem),safe=True )
            except Exception, e:
                log.msg("************* ERROR Submitting to mongoDB error: %s "%e, level=log.ERROR)
            try:
                # SUBMIT TO DB ONLY IF RESPONSE FROM SOLR
                page = urllib2.urlopen(req)
                #resultDB = self.db.items
		self.db.items.update({"url" : storeItem['url']},{"comments" : storeItem['comments'], "url" : storeItem['url']}, upsert=True)
		#lalinaDB = self.db.lalina
		print "****TYPE******"
		print type(clean)
		self.db.lalina.update({"key" : clean['key']}, clean, upsert=True, safe = True)
		log.msg("********* SOLR SUBMITTED ****** doc to solr with response %s "%page, level=log.DEBUG)
            except Exception, e:
                log.msg("***********ERROR Submitting to SOLR error: %s"%e, level=log.ERROR)
        else:
            log.msg("*********** Not commiting to solr or DB commit set to false  ",level=log.WARNING)

        return cleanItem
        

