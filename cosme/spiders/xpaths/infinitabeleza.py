from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class InfinitaBelezaXPath(AbstractXPath):
    
    META = {
    
    "image" : "//img[@id=\\'imgView\\']/@src",
    "name" : "//h1[@id=\\'nome-produto\\']/text()",
    "brand" : "//a[@class=\\'color\\']/strong/text()",
    "price" : "//span[@id=\\'variacaoPreco\\']/text()",
    "description" : "//p[1]/span/span/strong/span/text()",
    "category" : "null",
    "sku" : "//null",
    }

    COMMENTS = {
       "commentList":  "//ul[@class=\'produtoListaComentarios\']/li",
       "commenterName": ".//h3/span/text()",
       "commentText": ".//p/text()",
       "commentDate": ".//h3/text()",
       "commentStar": ".//div[contains(@class, 'avaliacaoProduto')]/@class"
    }
    
    def get_meta(self):
        return self.META

    def get_comments(self):
        return self.COMMENTS
