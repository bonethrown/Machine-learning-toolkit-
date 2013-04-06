from cosme.spiders.xpaths.belezanaweb import BelezanaWebXPath
from cosme.spiders.xpaths.infinitabeleza import InfinitaBelezaXPath
from cosme.spiders.xpaths.laffayette import LaffayetteXPath
from cosme.spiders.xpaths.magazineluiza import MagazineLuizaXPath
from cosme.spiders.xpaths.sepha import SephaXPath
from cosme.spiders.xpaths.sephora import SephoraXPath
from cosme.spiders.xpaths.sephora2 import Sephora2XPath    
class XPathRegistry:
    
    xpathDict = dict()
    
    def __init__(self):
        self.xpathDict['belezanaweb'] = BelezanaWebXPath()
        self.xpathDict['infinitabeleza'] = InfinitaBelezaXPath()
        self.xpathDict['laffayette'] = LaffayetteXPath()
        self.xpathDict['magazineluiza'] = MagazineLuizaXPath()
        self.xpathDict['sepha'] = SephaXPath()
        self.xpathDict['sephora'] = SephoraXPath()
        self.xpathDict['sephora2'] = Sephora2XPath()
        
    def getXPath(self, site):
        return self.xpathDict[site]        