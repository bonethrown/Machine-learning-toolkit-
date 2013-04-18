from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
class SephaXPath(AbstractXPath):
    META = {
    "image" : "//img[@id=\'imagem_descricao\']/@src",
    "name" : "//span[@class=\'nome\']/text()",
    "brand" : "//span[@class='fornecedor']/text()",
    "price" : "//span[@itemprop=\'price\']/text()",
    "description" : "//span[@id=\'textoDescricao\']/text()",
    "category" : "//h2[@class=\'titulo\']/a/text()",
    "sku" : "//span[@class=\'referencia\']/text()",
    "product_id": "//meta[@itemprop=\"productID\"]/@content"
    }

    COMMENTS = {
       "commentList"  : "//div[@class=\'comentarioBox\']",
       "commenterName": ".//div[@class=\'right-comments\']/div[@class=\'txt-avaliation\']/small[1]/text()",
       "commentText"  : ".//div[@class=\'right-comments\']/div[@class=\'content-comments\']/span[@class=\'txt-util\']/text()",
       "commentDate"  : ".//div[@class=\'right-comments\']/div[@class=\'txt-avaliation\']/small[2]/text()",
       "commentStar"  : ".//div[@class=\'produtosOpinioes\']/div[@itemprop=\'reviewRating\']/ul/li",
    }
    def get_meta(self):
        return self.META
    
    
    def get_comments(self):
        return self.COMMENTS

    ## 
    # With a 'por' highlighted price
    def get_price2(self):
        return "//div[@class=\"boxPrecoProduto\"]/span[2]/span/text()"