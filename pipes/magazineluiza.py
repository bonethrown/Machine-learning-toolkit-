"""
Pipelines per site are stored in their own folder for minumum chaos
"""

from utils import utils,categorizer
import re
from scrapy import log
from scrapy.exceptions import DropItem
import datetime

#Do all default processing here before going on to site specific processing.
def process(item,spider,matcher):


    if item['name']:
        temp = item['name']
        item['name'] = temp[0]

    #if there isn't a price make it very expensive 
    if item['price']:
        item['price'] = float(utils.getFirst(item['price']).replace(',','.'))
        
    if item['brand']:
         temp = item['name']
        # temp = temp[0]
         item['brand'] = matcher.listMatch(temp)
         log.msg("match found: %s" %item['brand'], level=log.DEBUG)
    
    # item["raw_data"] = ""
    #set our crawl time
    item['date_crawled'] = utils.convertDateClass(datetime.datetime.today().isoformat())
     
    #is this a gay video?
        
        
    return item
         
    #except:
    #    log.msg("Error parsing results", level=log.WARNING)
    #   raise DropItem("Something whent wrong parsing dropping item %s " % item['url'])
    
