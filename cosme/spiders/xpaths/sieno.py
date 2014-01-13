from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class Sieno(AbstractXPath):
    META = {
        
    "image" : "//img[@id='image']/@src",
    "name"  : "//div[@class='clear product_title']/h5/text()",
    "brand" : "//a[@class='manufacturer']/img/@alt",			
    "price" : "//span[@class='price']/text()",
    "description" : "//div[@class='clear product_description']/text()",
    "category" : "//div[@id='breadcrumb']/a[2]/text()",
    "sku"   : "//button[@class='button']/@value",		
    "volume" : "//td[@class='product_name']/span/b/text()"
    }


    
