
from utils import utils,categorizer
import re
from scrapy import log
from scrapy.exceptions import DropItem
import datetime

#do all default processing here
def process(item,spider,matcher):

    for key in item.keys():
        if item[key]:
            item[key] = utils.getFirst(item[key])

    if item['name']:
        tempNameArr = item['name']

        return item

