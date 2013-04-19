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
		if isinstance(item['name'], list):
			temp = item['name']
			item['name'] = temp[0].lower()
		else:
			item['name'] = item['name'].lower()
        #if there isn't a price make it very expensive 
        if item['price']:
		temp = utils.getFirst(item['price'])
		if isinstance(temp, float):
			item['price'] = temp 
		else:
			temp = temp.replace(',','.')
			temp = float(temp) 
			item['price'] = temp
	if item['brand']:
		if isinstance(item['brand'], list):
			temp = item['brand']
			item['brand'] = temp[0].lower()
		else:
			item['brand'] = item['category'].lower()
		# item['brand'] = matcher.listMatch(temp)
        if item['url']:
            item['url'] = item['url'].lower()
        
	if item['category']:
		if isinstance(item['category'], list):
			temp = item['category']
			item['category'] = temp[0].lower()
		else:
			item['category'] = item['category'].lower()
	
	item['date_crawled'] = utils.convertDateClass(datetime.datetime.today().isoformat())
         
        #is this a gay video?
            
            
        return item
             
        #except:
        #    log.msg("Error parsing results", level=log.WARNING)
        #   raise DropItem("Something whent wrong parsing dropping item %s " % item['url'])
        
