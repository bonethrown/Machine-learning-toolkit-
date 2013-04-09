# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

##remember to import new added pipes
import sys
from scrapy import log
from pipes import default
import json, urllib2
from  pipes.utils import db,utils
import os
from cosme.pipes.belezanaweb import BelezanaWeb
from cosme.pipes.sephora import SephoraSite
from cosme.pipes.magazineluiza import MagazineLuizaSite
from cosme.pipes.infinitabeleza import InfiniteBeleza
from cosme.pipes.default import AbstractSite



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
        self.siteDict['inifitebeleza'] = InfiniteBeleza()
        self.siteDict['default'] = AbstractSite()
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
   	print "***********CLEAN ITEM *************"
	print cleanItem 
        #cleanItem = self.defaultSite.process(cleanItem,spider)
        #Separate Store for raw data
        #storeItem  = {}
        #storeItem['url'] = cleanItem['url']
        #storeItem['raw_data'] = cleanItem['raw_data']
        #package to JSON and encode
        arrItem = []
        arrItem.append(dict(cleanItem))

        
        #log.msg("Item ready for json %s "%arrItem, level=log.DEBUG)
        singleItemJson = json.dumps(arrItem)
        #log.msg("Getting ready to send %s "%singleItemJson, level=log.DEBUG)

        if commit:
            #Send Data to MongoDB
            try:
                req  = urllib2.Request(self.solr_url, data = singleItemJson)
                req.add_header("Content-type", "application/json")
                #send data to MongoDB vids collection (sample use nubunu_db; db.vids.find();)
                resultDB = self.db.items.insert(dict(cleanItem),safe=True )
                #resultDB_raw = self.db.vids_raw.insert(dict(storeItem),safe=True )
                log.msg("Submitting to mongoDB ready to send %s type %s  result %s " %
                                (cleanItem,type(cleanItem),resultDB), 
                            level=log.DEBUG)
            except Exception, e:
                log.msg("ERROR Submitting to mongoDB error: %s "%e, level=log.ERROR)
                try:
                    #lets see what we got
                    page = urllib2.urlopen(req)
                    log.msg("********* SOLR SUBMITTED ****** doc to solr with response %s "%page, level=log.DEBUG)
                except Exception, e:
                    log.msg("***********ERROR Submitting to SOLR error: %s"%e, level=log.ERROR)
        else:
            log.msg("Not commiting to solr or DB commit set to false  ",level=log.WARNING)

        return cleanItem
        

