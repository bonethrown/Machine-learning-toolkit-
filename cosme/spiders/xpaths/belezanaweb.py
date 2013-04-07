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
            }
    
    def get_meta(self):
        return self.META

    COMMENTS = {
       "commentList":  "//div[@id=\'comentarios\']/ul",
       "commenterName": ".//li[@id=\'star\']/div[@class=\'dados\']/span/text()",
       "commentText": ".//li[2]/text()",
       "commentDate": ".//li[@id=\'star\']/div[@class=\'dados\']/text()",
       "commentStar": ".//li[@id=\'star\']/div[1]/@class"
    }

    
    def get_comments(self):
        return self.COMMENTS
