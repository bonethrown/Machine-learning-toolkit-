from scrapy import signals
from scrapy.exceptions import NotConfigured
from cosme.pipes.utils import db2

DEFAULT_ANALYTICS_DB = "analytics"
SPIDER_PREFIX = "spd"
class Analytics(object):


    def __init__(self, stats, db_name):
        self.items_scraped = 0
	self.stats = stats
	self.db = db2.getConnection(db_name)

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('ANALYTICS_ENABLED'):
            raise NotConfigured
	
	ANALYTICS_DB = crawler.settings.get("ANALYTICS_DB",DEFAULT_ANALYTICS_DB)

        # instantiate the extension object
        ext = cls(crawler.stats,ANALYTICS_DB)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        print "##opened spider analytics enabled %s" % spider.name

    def spider_closed(self, spider):
        spider.log("closed spider %s" % spider.name)
	try:
		self.db[SPIDER_PREFIX+spider.name].insert(self.stats.get_stats())
	except Exception, e:
		print "Error submitting to DB stats :%s"%e

    def item_scraped(self, item, spider):
        self.items_scraped += 1

