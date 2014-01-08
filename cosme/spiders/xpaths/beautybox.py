from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class BeautyBoxXPath(AbstractXPath):

    META = {
    "image" : "//img[@class=\'zoom\']/@src",
    "name" : "//div[@class='descr_prod']/h1/span/text()",

    "brand" : "//div[@class='descr_prod']/h2/p/span/text()",
    "price" : "//p[@class='preco2']/text()",
    "description" : "//div[@id=\'dv_descricao\']/p[1]/span/text()",
    "category" : "//div[@class='breadcrumb']/ul/li[3]/a/span[@class='title']/text()",
    "sku" : "//div[@class='descr_prod']/p[1]/span[@id='spnSku']/text()",
    "volume" : "//div[@class='tamanhoPrd']/input",
    "product_id": "//meta[@itemprop=\"productID\"]/@content"
    }

    COMMENTS = {
       "commentList"  : "//div[@class='content ']/p[@class='descricao']/text()",
       "commenterName": "//p[@class='autor']/strong/text()",
       "commentText"  : ".//div[@itemprop=\'description\']/text()",
       "commentDate"  : "//meta[@itemprop=\"datePublished\"]/@content",
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

