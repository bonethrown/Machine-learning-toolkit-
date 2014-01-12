from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup

class SubmarinoXPath(AbstractXPath):

    META = {
    "image" : "//figure[@class='main-product-photo']/a/img[@class='photo']/@src",
    "name" : "//h1[@class='title-product']/text()",
    "brand" : "//div[@class='title-box']/a/text()",
    "price" : "//li[@class='pl-li sale-price']/strong[@class='price-val']/span[@class='amount']",
    "description" : "//div[@class='content']/p[2]/text()",
    "category" : "//span[@class=\'span-bc\'][2]/a/text()",
    "sku" : "//small[@class='cod-prod sku']/text()",
    "volume" : "//article/table",
    "product_id": "//h1[@class='title-product']"
    }

    #########################################
    # VOLUME is contained in the NAME
    # Volume xpath is  only info that's not clean
    # the volume xpath is too dirty. BUT it is   
    # availabre in the name of the product
    ##########################################

