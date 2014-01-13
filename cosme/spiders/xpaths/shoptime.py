from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class Shoptime(AbstractXPath):
    META = {
        
    "image" : "//img[@id='imgProduto']/@src",
    "name"  : "//h1[@class='title']/text()",
    "brand" : "//div[@class='piBox close']/text()",	
    "price" : "//span[@class='val']/strong[@class='pv']" ,
    "description" : "//div[@class='piBox']/p/text()",
    "category" : "//meta[@name='description']/@content",
    "sku"   : "//div[@class='piBox close']/text()",
    "volume" : "//h1[@class='title']/text()"
    }


    
