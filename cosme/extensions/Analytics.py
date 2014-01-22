from scrapy import signals
from scrapy.exceptions import NotConfigured
from cosme.pipes.utils import db2
from scrapy.mail import MailSender
import socket


DEFAULT_ANALYTICS_DB = "analytics"
DEFAULT_DBCOLLECTION = "crawlstats"
EMAIL =  True

class Analytics(object):


    def __init__(self, stats, db_name,db_collection,mailer):
        self.items_scraped = 0
	self.stats = stats
	self.db = db2.getConnection(db_name)
	self.dbcollection = db_collection
	self.mailer = mailer

    @classmethod
    def from_crawler(cls, crawler):
	mailer = MailSender()
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('ANALYTICS_ENABLED'):
            raise NotConfigured
	
	ANALYTICS_DB = crawler.settings.get("ANALYTICS_DB",DEFAULT_ANALYTICS_DB)
	ANALYTICS_DBCOLLECTION = crawler.settings.get("ANALYTICS_DBCOLLECTION",DEFAULT_DBCOLLECTION)

        # instantiate the extension object
        ext = cls(crawler.stats,ANALYTICS_DB,ANALYTICS_DBCOLLECTION,mailer)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        print "##opened spider analytics enabled %s" % spider.name
	self.stats.set_value('hostname', socket.gethostname())
	self.stats.set_value('name', spider.name)
	self.mailer.send(to=["atilev@gmail.com"], subject="scrapy test email", body="Some body")

    def spider_closed(self, spider):
        spider.log("closed spider %s" % spider.name)
		
	try:
		cleanStats = self.cleanItems(self.stats.get_stats())
		self.db[self.dbcollection].insert(cleanStats)
	except Exception, e:
		print "Error submitting to DB stats :%s"%e

    def item_scraped(self, item, spider):
        self.items_scraped += 1

   #Mongo doesn't like . chars to lets remove them
    def cleanItems(self, itemDict):
	cleanChars = ['.','-']
	replacementChar = "-"
	cleanResult = {}	
	for key in itemDict.keys():
		origKey = key
		for val in cleanChars:
			key = key.replace(val,replacementChar)
		cleanResult[key] = itemDict[origKey]
	return cleanResult


if __name__ == '__main__':
	an = Analytics("","analytics","crawlerstats","")
	teststr = {"thi.is.a.test.query.":"another.tet.string"}
	print "running test %s"%teststr
	print an.cleanItems(teststr)
		

	
