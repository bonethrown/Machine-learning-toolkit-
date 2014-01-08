from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
from BeautifulSoup import BeautifulSoup
class MeuEspelhoXPath(AbstractXPath):

    META = {
    "image" : "//div[@id=\'img-detalhe\']/img/@src",
    "name" : "//div[@class='container detail']/h2/span",
    "brand" : "//div[@class='container detail']/h2",
    "price" : "//div[@id='comprar-desc']/p[1]/strong",
    "description" : "//div[@class='desc']/p[1]/span",
    "category" : "//div[@class=\'bread-crumb\']/p/a[@class='nv2']",
    "sku" : "",
    "volume" : "//div[@class='tamanhoPrd']/input",
    "product_id": ""
    }


    # With a 'por' highlighted price

