"""
Pipelines per site are stored in their own folder for minumum chaos
"""

from utils import utils
from scrapy.exceptions import DropItem
from scrapy import log
import datetime
import pipeMethods

class AbstractSite:
    
    #Do all default processing here before going on to site specific processing.
    def process(self, item, spider):
        
	if not item['price']:
            	item['price'] = 'NA' 
		#raise DropItem("missing price DROPPING")
        
	if  not item['name']:
            raise DropItem("Missing name in %s . Dropping" % item['url'])
	
	if item['name']:
		item['name'] = pipeMethods.genericNameExtract(item['name'])

        #if not item['brand']:
		#raise DropItem("missing brand in %s . Dropping this" % item)
        
	#De-array these values. 
        #if isinstance(item['description'],list) and len(item['description']) > 1:
         #   item['description'] = item['description'].pop()

	if item['volume']:
		if not utils.hasCheckVolume(item['volume']):
			item['volume'] = ''
	if not item['volume']: 
		item['volume'] = pipeMethods.nonXpathVolume(item['name'], item['url'])
	
	item['date_crawled'] = utils.convertDateClass(datetime.datetime.today().isoformat())
	return item
        #except:
        #    log.msg("Error parsing results", level=log.WARNING)
        #   raise DropItem("Something whent wrong parsing dropping item %s " % item['url'])
       # 
