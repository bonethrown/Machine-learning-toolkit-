from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
class MagazineLuizaXPath(AbstractXPath):
    META = {
            "image" : "//div[@class=\'big-picture-first-image\']/a/@href",
    
            "name" :  "//div[@class=\'container-title-product-detail\']/h1/text()",
    
            "brand" : "//div[@class=\'fs-row\'][1]/div[@class=\'fs-right\']/div[1]/p/text()",
    
            "price" : "//span[@class=\'right-price\']/strong/text()",
    	    
	    "comments" : "//null",
            
	    "description" : "//strong[@class=\'fs-presentation\']/text()" ,
    
            "category" : "//ul[@class='breadcrumb breadcrumb-list-product']/li[@class='category']/a/text()" ,
    
            "sku" : "//div[@class=\'container-title-product-detail\']/small/text()" ,
            }
    
    def get_meta(self):
        return self.META
