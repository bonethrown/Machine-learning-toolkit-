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
       "commentList"  : "//div[@id=\'opinioes_lista_counteudo\']/div",
       "commenterName": ".//div[@class=\'nome\']/span[@itemprop=\'author\']/text()",
       "commentText"  : ".//div[@itemprop=\'description\']/text()",
       "commentDate"  : ".//div[@class=\'nome\']/text()",
       "commentStar"  : ".//div[@itemprop=\'reviewRating\']/ul/li",
    }
    def get_meta(self):
        return self.META
    
    
    def get_comments(self):
        return self.COMMENTS

    ## 
    # With a 'por' highlighted price
    def get_price2(self):
        return "//div[@class=\"boxPrecoProduto\"]/span[2]/span/text()"