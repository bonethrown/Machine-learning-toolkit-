from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class InfinitaBelezaXPath(AbstractXPath):
    
    META = {
    
    "image" : "//img[@id='imgView']/@src",
    "name" : "//h1[@id='nome-produto']/text()",
    "brand" : "//span[@class='dados-valor brand']/a/strong/text()",
    "price" : "//span[@id='variacaoPreco']/text()",
    "description" : "//div[@id='descricao']",
    "comments":  "//div[@id=\"coments\"]",
    "category" : "//span[@class='link_itens'][1]/a/text()",
    "volume" : "//h1[@id='nome-produto']/text()"
    }

    COMMENTS = {
       "commentList"  : ".//div[@class=\'hreview']",
       "commenterName": ".//span[@class=\'reviewer']/h3/text()",
       "commentText"  : ".//span[@class=\'description']/text()",
       "commentDate"  : ".//span[@class=\'nonexistent']/text()",
       "commentStar"  : ".//div[@class=\'ranking']/span[1]/@class"
    }
    
    def get_meta(self):
        return self.META

    def get_comments(self):
        return self.COMMENTS
