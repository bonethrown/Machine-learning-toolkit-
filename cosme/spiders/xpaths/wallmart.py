from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class Wallmart(AbstractXPath):
    META = {
    
    "image" : "//img[@class='main-picture']/@src",
    "name" :  "//div[@class='product-title-header']/h1/text()",
    "brand" : "//a[@class='product-brand']/text()",
    "price" : "//span[@class='payment-price']/strong/span/text()",
    "description" : "//td[@class='value-field Outras-Informacoes']",
    "category" : "//td[@class='value-field Tipo']/text()",
    "sku" : "//td[@class='value-field Referencia-do-Modelo']/text()",
    "volume": "//div[@class='product-title-header']/h1/text()"
    }

    def get_meta(self):
        return self.META
    
