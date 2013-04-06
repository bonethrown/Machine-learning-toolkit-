from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class InfinitaBelezaXPath(AbstractXPath):
    
    META = {
    
    "image" : "//img[@id=\\'imgView\\']/@src",
    "name" : "//h1[@id=\\'nome-produto\\']/text()",
    "brand" : "//a[@class=\\'color\\']/strong/text()",
    "price" : "//span[@id=\\'variacaoPreco\\']/text()",
    "start" : "//null",
    "description" : "//p[1]/span/span/strong/span/text()",
    "category" : "null",
    "sku" : "//null",
    }

    def get_meta(self):
        return self.META
