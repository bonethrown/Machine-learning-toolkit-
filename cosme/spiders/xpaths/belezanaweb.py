from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class BelezanaWebXPath(AbstractXPath):
    META = {
    "image" : "//img[@id=\'imagem4\']/@src",
    "name" : "//h1[@class=\'title-product\']/text()",
    "brand" : "//span[@class='fornecedor']/text()",
    "price" : "//li[@class='preco-promocao']",
    "description" : "//span[@id=\'textoDescricao\']/text()",
    "category" : "//h2[@class=\'titulo\']/a/text()",
    "sku" : "//input[@class='radio radioTamanhos opcoesProduto']/@value",
    "volume" : "//div[@class='tamanhoPrd']/input",
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

    # With a 'por' highlighted price
    def get_price2(self):
        return "//div[@class=\"boxPrecoProduto\"]/span[2]/span/text()"
    def get_price3(self):
	return "//div[@class='boxPrecoProduto precoNormal']"
    def get_price4(self):
	return "//div[@class='boxPrecoProduto']"
    
    def get_volume2(self):
	return "//span[@class=\'tamanho\']"
    def get_name2(self):
	return "//div[@class='nomeProduto']/h1[@class='marginLeft10 left']/text()"

