
from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class CabelezaXPath(AbstractXPath):
    META = {
    "image" : "//img[@id=\\'ProdutoImageAux\\']/@src",
    "name" : "//h2[@class=\\'titProduto\\']/text()",
    "brand" : "//dd[1]/a/text()",
    "price" : "",
    "description" : "",
    "category" : "",
    "sku" : "",
    "volume" : "",
    "product_id": "",
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


#PRICE = "//span[@id=\\'spanPrecoPor\\']/strong/text()"\
#STARS="//a[@class=\\'Avaliar iframe\\']"\
#DESCRIPTION = "//div[@id=\\'ProductDescription\\']/p/font[2]/text()"\
#CATEGORY="ul[@id='breadcrumbs']/li[2]/strong/text()"\
#SKU="//dl[@class='lstReference']/dd[2]/text()"\
