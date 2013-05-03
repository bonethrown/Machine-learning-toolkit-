from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class BelezanaWebXPath(AbstractXPath):
    META = {
            "image" : "//img[@id=\'imagem4\']/@src",
    
            "name" :  "//div[@class=\'title\']/h1/text()",
    
            "brand" : "//div[@class=\'header\']/span/a/text()",
    
            "price" : "//div[@class=\'prices\']/div[2]/div/span/text()",
    
            "description" : "//div[@class=\'text\']/p/text()",
    
            "category" : "//div[@class=\'content\']/ul/li[2]/a/text()" ,
    
            "sku" : "//div[@class=\'title\']/p/text()" ,
            
            "comments":  "//div[@class=\"rateAndTips\"]",

	    "volume" : "//div[@class='prices']/div[1]",
            }
    
    def get_meta(self):
        return self.META

    COMMENTS = {
       "commentList":  "//div[@class=\"rate\" or @class=\"mainRate\"]",
       "commenterName": ".//div[@class=\'content\']/div[@class=\'stars\']/span[2]/text()",
       "commenterName2": ".//div[@class=\'stars\']/span[2]/text()",
       "commentText": ".//div[@class=\'content\']/div[@class=\'text\']/div/p/text()",
       "commentText2": ".//div[@class=\'text\']/div/p/text()",
       "commentDate": ".//li[@id=\'star\']/div[@class=\'dados\']/text()",
       "commentStar": ".//div[@class=\'content\']/div[@class=\'stars\']/span/img",
       "commentStar2": ".//div[@class=\'stars\']/span/img"
    }

    
    def get_comments(self):
        return self.COMMENTS
