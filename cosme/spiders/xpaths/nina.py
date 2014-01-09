from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class AZXPath(AbstractXPath):

    META = {
    "image" : "//div[@id='product-zoom-box']/img/@src",
    "name" : "//h1[@class='product-title-product']/text()",
    "brand" : "//td/a[@class='EstNomeCat']/text()",
    "price" : "",
    "description" : "//div[@id='detail-description']/p/text()",
    "category" : "//span[@class='AdicItem']/text()",
    "sku" : "",
    "volume" : "//span[@class='AdicItem']/text()",
    "product_id": ""
    }


    # With a 'por' highlighted price

