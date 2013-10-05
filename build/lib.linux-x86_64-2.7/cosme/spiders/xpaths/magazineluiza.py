from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
class MagazineLuizaXPath(AbstractXPath):
    META = {
            "image" : "//div[@class=\'big-picture-first-image\']/a/@href",
    
            "name" :  "//div[@class=\'container-title-product-detail\']/h1/text()",
    
            "brand" : "//div[@class=\'fs-row\'][1]/div[@class=\'fs-right\']/div[1]/p/text()",
    
            "price" : "//span[@class=\'right-price\']/strong/text()",
    	    
	    "description" : "//div[@class='factsheet-container  active']" ,
    
            "category" : "//ul[@class='breadcrumb breadcrumb-list-product']/li[@class='category']/a/text()" ,
    
            "sku" : "//div[@class=\'container-title-product-detail\']/small/text()" ,
            
            "comments": "//div[@class=\'container-seeing-comments\']",
    
            "volume": "//span[@class=\'btn-default\' and input[@checked=\'checked\']]/span/text()"
            }

    COMMENTS = {
       "commentList":  "//div[@class=\"container-seeing-comments\"]/div",
       "commentList2": "//div[@class=\"container-rate-stars\"]/div[@class=\'content-rate-stars\']",
       "commenterName": ".//div[@class=\'right-comments\']/div[@class=\'txt-avaliation\']/small[1]/text()",
       "commenterName2": ".//div[@class='\non-existent']/text()",
       "commentText": "//div[@class='txt-avaliation']/p[@itemprop='description']/text()",
       "commentText2": ".//div[@class=\'content-rate-stars\']/div[@class=\'content-i-evaluate\']/span/text()",
       "commentDate": ".//div[@class=\'right-comments\']/div[@class=\'txt-avaliation\']/small[2]/text()",
       "commentStar": "//div[@class='left-comments']/span[@class='star-comments rateing sprite-stars star-medium']/meta/@content",
       "commentStar2": ".//div[@class=\'content-rate-stars\']/div[@class=\'principal-rate\']/span[@class=\'principal-star\']/em[@class=\'sprite-stars\']/@style",
    }
        
    def get_meta(self):
        return self.META

    def get_comments(self):
        return self.COMMENTS
