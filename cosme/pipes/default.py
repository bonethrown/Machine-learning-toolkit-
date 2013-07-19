"""
Pipelines per site are stored in their own folder for minumum chaos
"""

from utils import utils
from scrapy.exceptions import DropItem
from scrapy import log
import datetime

class AbstractSite:
    
    #Do all default processing here before going on to site specific processing.
    def process(self, item, spider):
        if  not item['name']:
            raise DropItem("Missing name in %s . Dropping" % item)
        #De-array these values. 
        if isinstance(item['description'],list) and len(item['description']) > 0:
            item['description'] = item['description'].pop()
        # match For Brand
        #if there isn't a price make it very expensive 
        if not item['price']:
            raise DropItem("missing price DROPPING")
        if not item['brand']:
            raise DropItem("missing brand in %s . Dropping this" % item)
	if item['name']:
		if isinstance(item['name'], list):
			temp = item['name']
			item['name'] = temp[0].lower()
		else:
			item['name'] = item['name'].lower()
			tempName = item['name'] 
	# item["raw_data"] = ""
        #set our crawl tim
	item['date_crawled'] = utils.convertDateClass(datetime.datetime.today().isoformat())
        
	return item
        #except:
        #    log.msg("Error parsing results", level=log.WARNING)
        #   raise DropItem("Something whent wrong parsing dropping item %s " % item['url'])
       # 
