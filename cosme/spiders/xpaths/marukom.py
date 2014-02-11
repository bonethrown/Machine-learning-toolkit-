from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class Marukom(AbstractXPath):
    META = {
    
    "image" : "//img[@class='main-picture']/@src",
    "name" :  "//div[@class='product-name']/h1/text()",
    "brand" : "//div[@class='marca']//@title",
    "price" : "//span[@class='price']/text()",
    "description" : "//div[@class='short-description']/p",
    "category" : "//div[@class='breadcrumbs']/a/text()",
    "sku" : "",
    "volume": "//div[@class='product-name']/h1/text()"
    }



    def get_meta(self):
        return self.META
    

    # With a 'por' highlighted price
    def get_price2(self):
        return "//span[@class='price']/text()"

