from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class Netfarma(AbstractXPath):
    META = {
        
    "image" : "//img[@id='imagemProduto']/@src",
    "name"  : "//div[@class='informacoes']/p[@class='nome']/text()",
    "brand" : "//div[@class='informacoes']/p[@class='nome']/text()",	
    "price" : "//span[@id='PrecoPromocaoProduto']/text()",
    "description" : "//div[@class='resumida']",
    "category" : "//meta[@name='description']/@content",
    "sku"   : "//div[@class='codbrand']/p[@class='codigo']/text()",
    "volume" : "//div[@class='informacoes']/p[@class='gramatura']/text()"
    }


    
