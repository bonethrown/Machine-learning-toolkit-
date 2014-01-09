from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class MeuEspelhoXPath(AbstractXPath):

    META = {
    "image" : "//div[@id=\'img-detalhe\']/img/@src",
    "name" : "//div[@class='container detail']/h2/span/text()OK",
    "brand" : "//div[@class='container detail']/h2text()OK",
    "price" : "//div[@id='comprar-desc']/p[1]/strong",
    "description" : "//div[@id='tab2']/div[@class='desc']/p/text()OK",
    "category" : "//div[@class=\'bread-crumb\']/p/a[@class='nv2']/text()OK",
    "sku" : "",
    "volume" : "//div[@id='tab1']/div[@class='cores']/ul/li/strong/text()OK",
    "product_id": ""
    }


    # With a 'por' highlighted price

