from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class DafitiXPath(AbstractXPath):

    META = {
    "image" : "//div[@id='product-zoom-box']/img/@src",
    "name" : "//h1[@class='product-title-product']/text()",
    "brand" : "//div[@class='product-title-brand']/text()",
    "price" : "//div[@class='product-title-brand']/text()",
    "description" : "//div[@id='detail-description']/p/text()",
    "category" : "//li[@class='product-information-item'][4]/text()",
    "sku" : "//li[@class='product-information-item'][1]/text()",
    "volume" : "//div[@id='productSizeSelector']/div/text()",
    "product_id": "//div[@class='product-title-brand']/text()"
    }


    #########################
    #Price is javascript loaded   
    ##########################
