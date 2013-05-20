from pymongo import Connection
import os,sys,urllib2
import time
import json


def feedtoSolr(batch):
    solr_url = "http://localhost:8080/solr/cosme0/update?json"
    fail = False
    try:
        req  = urllib2.Request(solr_url, data = batch)
        req.add_header("Content-type", "application/json")
        #lets see what we got
        page = urllib2.urlopen(req)
        print "##solr response: %s"%(page)
    except Exception,e :
        print "problem sending batch %s"%e
        print batch
        fail = True
    return fail


def dumpToJson(batch,*fields):

    try:
        fp = open()
        req.add_header("Content-type", "application/json")
        #lets see what we got
        page = urllib2.urlopen(req)
        print "##solr response: %s"%(page)
    except Exception,e :
        print "problem sending batch %s"%e
        print batch

#set our batch size
def  createBatch(db,limit=10):
   print "starting process"
   start = time.time()
   head = 0
   count = 1
   batch = []
   status = False
   print "db count"
   print db.lalina.count()
   for doc in  db.lalina.find():
     count = count + 1
     #print type(doc)
     if count % limit == 0 :
        print "## processed %s docs"%count
        batchJson = json.dumps(batch)
        status = feedtoSolr(batchJson)
        #if batch fails submit each doc individually
        if not status:
            for single in batch:
                 batchJson = json.dumps(single)
                 feedtoSolr(batchJson)
        del batch
        batch = []

     else:

         del doc['_id']
         # do this so solr doesn't complain. Though I'm sure there is a way to prevent this in solr
         if not doc.has_key('image'):
            doc['image'] = ""
         batch.append(dict(doc))
   end = time.time()
    #print "feeding finisehd in %s ms"%(end-start)

def main(batchSize):
        connection = Connection()
        lalina = connection.comments_db
	createBatch(lalina, limit=batchSize)

#if __name__ == "__main__":

    #first argument: batch size
    #second argument: dmp or feed
    #third argument : filename
 #   main(int(sys.argv[1]))
