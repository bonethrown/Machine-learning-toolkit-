"""
Pipelines per site are stored in their own folder for minumum chaos
"""

from utils import utils,categorizer
import re
from scrapy import log
from scrapy.exceptions import DropItem
import datetime

#Do all default processing here before going on to site specific processing.
def process(item,spider):
    if  not item['name']:
        raise DropItem("Missing name in %s dropping" % item)
    #De-array these values. 
    if isinstance(item['description'],list) and len(item['description']) > 0:
        item['description'] = item['description'].pop()
    # match For Brand
    #if there isn't a price make it very expensive 
    if not item['price']:
        item['price'] = 1000
    if not item['brand']:
        raise DropItem("missing brand in %s dropping this" % item)

    
    # item["raw_data"] = ""
    #set our crawl time
    item['date_crawled'] = utils.convertDateClass(datetime.datetime.today().isoformat())
     
    #is this a gay video?
        
        
    return item
         
    #except:
    #    log.msg("Error parsing results", level=log.WARNING)
    #   raise DropItem("Something whent wrong parsing dropping item %s " % item['url'])
    
