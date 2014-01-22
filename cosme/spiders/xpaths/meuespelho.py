from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class MeuEspelhoXPath(AbstractXPath):

    META = {
    "image" : "//img[@id='image-main']/@src",
    "name" : "//div[@class='tpl-product-name']/h1/div/text()",
    "brand" : "//div[@class='tpl-ref-container']//div/a/text()",
    "price" : "//em[@class='valor-por']/strong/text()",
    "description" : "//div[@class='tpl-short-description']/div/text()",
    "category" : "//div[@class='bread-crumb']/ul/li/a/text()",
    "sku" : "//input[@id='___rc-p-sku-ids']/@value",
    "volume" : "//div[@class='nomeSku']/text()",
    "product_id": "//input[@id='___rc-p-sku-ids']/@value"
    }


    def get_price2(self):
        return "//em[@class='valor-dividido']/strong[2]/text()"
