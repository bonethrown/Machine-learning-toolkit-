from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class LooshoXPath(AbstractXPath):

    META = {
    "image" : "//a[@class='jqzoom zoomThumbActive']/img/@src",
    "name" : "//div[@class='content']/div[@class='in']/div[@class='meio']/h1/text()",
    "brand" : "//span[@id='j_id59']/a/span/text()",
    "price" : "//div[@class='valores']/span[@class='valorPor']",
    "description" : "//div[@class='inner-descricao']",
    "category" : "//div[@class='breadcrumb']/strong/a[3]",
    "sku" : "",
    "volume" : "",
    "product_id": ""
    }


    ##################
    #VOLUME is always the last 
    #paragraph of the DESCRIPTION
    ##################
