from belezanaweb import BelezanaWebXPath
from infinitabeleza import InfinitaBelezaXPath
from laffayette import LaffayetteXPath
from magazineluiza import MagazineLuizaXPath
from sepha import SephaXPath
from sephora2 import Sephora2XPath  
from walmart import Walmart  
from americanas import Americanas 
from submarino import SubmarinoXPath
from dafiti import DafitiXPath
from netfarma import Netfarma


class XPathRegistry:
    
    xpathDict = dict()
    
    def __init__(self):
        self.xpathDict['belezanaweb'] = BelezanaWebXPath()
        self.xpathDict['infinitabeleza'] = InfinitaBelezaXPath()
        self.xpathDict['laffayette'] = LaffayetteXPath()
        self.xpathDict['magazineluiza'] = MagazineLuizaXPath()
        self.xpathDict['sepha'] = SephaXPath()
        self.xpathDict['sephora'] = Sephora2XPath()
        self.xpathDict['walmart'] = Walmart()
        self.xpathDict['americanas'] = Americanas()
        self.xpathDict['submarino'] = SubmarinoXPath()
        self.xpathDict['dafiti'] = DafitiXPath()
        self.xpathDict['netfarma'] = Netfarma()
        #self.xpathDict['sephora2'] = Sephora2XPath()
        
    def getXPath(self, site):
        return self.xpathDict[site]        
