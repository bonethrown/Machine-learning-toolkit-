"""
Pipelines per site are stored in their own folder for minumum chaos
"""

from utils import utils
from scrapy import log
import datetime
from cosme.pipes.default import AbstractSite

class MagazineLuizaSite(AbstractSite):
    
    #Do all default processing here before going on to site specific processing.
    def process(self, item,spider,matcher):
    
    
        if item['name']:
            temp = item['name']
            item['name'] = temp[0]
    
        #if there isn't a price make it very expensive 
        if item['price']:
            item['price'] = float(utils.getFirst(item['price']).replace(',','.'))
            
        if item['name']:
            temp = item['name']
            log.msg("match found: %s" %temp, level=log.DEBUG)
            item['brand'] = matcher.listMatch(temp)
            #log.msg("match found: %s" %item['brand'], level=log.DEBUG)
            log.msg(item['brand'])
    
        if item['url']:
            item['url'] = item['url'].lower()
        # item["raw_data"] = "
        #set our crawl time
        item['date_crawled'] = utils.convertDateClass(datetime.datetime.today().isoformat())
         
        #is this a gay video?
            
            
        return item
             
        #except:
        #    log.msg("Error parsing results", level=log.WARNING)
        #   raise DropItem("Something whent wrong parsing dropping item %s " % item['url'])
        
