from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class Americanas(AbstractXPath):
    META = {
    
    "image" : "//div[@class='prodImage']/a/img[@id='imgProduto']/@src",
    "name" :  "//div[@class='wtit']/h1[@class='title']/text()", 
    "brand" : "//div[@class='infoProd']/dl/dd[1]",
    "price" : "//p[@class='sale']/strong/span[@class='price']",
    "description" : "//div[@class='infoProd']/p",
    "category" : "//li[@class='category selected']/a[@class='link']/text()",
    "sku" : "//em[@class='identifier']/span[@class='id']",
    "volume":"//div[@class='infoProd']/dl/dd[5]/text()"
    }


    
