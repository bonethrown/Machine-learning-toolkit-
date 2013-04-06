
from utils import utils
from cosme.pipes.default import AbstractSite

class InfiniteBeleza(AbstractSite):
    #do all default processing here
    def process(self, item,spider,matcher):
    
        for key in item.keys():
            if item[key]:
                item[key] = utils.getFirst(item[key])
    
        if item['name']:
            tempNameArr = item['name']
    
        return item
    
