from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class BelezanaWebXPath(AbstractXPath):

    META = {
    "image" : "//div[@class='pics']/a/img[@class='zoom']/@src",
    "name"  : "//h1[@class='title-product']/text()",
    "brand" : "//div[@class='marca_produto']/a/img/@alt",
    "price" : "//li[@class='preco_normal']",
    "description" : "//div[@id='descricao_conteudo']/p",
    "category" : "//div[@class='breadcrumbs']/ul/li/text()",
    "sku"   : "//span[@id='cod_subproduto']/text()",
    "volume": "//ul[@class='tamanho']/li/a/text()",
    "product_id" : "//div[@class='footer_tooltip']/ul/li/text()"    
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
        #return "//div[@class=\"boxPrecoProduto\"]/span[2]/span/text()"
        return "//ul[@class='promocao']/li[@class='preco_promocao']"
    def get_price3(self):
	return "//div[@class='boxPrecoProduto precoNormal']"
    def get_price4(self):
	return "//div[@class='boxPrecoProduto']"
    
    def get_volume2(self):
	return "//span[@class=\'tamanho\']"
    def get_name2(self):
	return "//div[@class='nomeProduto']/h1[@class='marginLeft10 left']/text()"

    #added on January 13th
    def get_description2(self):
        return "//div[@id='descricao']"

    def get_product_id2(self):
	return "//div[@class='result_choices']/p/text()"	
