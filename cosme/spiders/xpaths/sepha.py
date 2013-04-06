from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
class SephaXPath(AbstractXPath):
    META = {
    "image" : "//img[@id=\'imagem_descricao\']/@src",
    "name" : "//span[@class=\'nome\']/text()",
    "brand" : "//span[@class='fornecedor']/text()",
    "price" : "//div[@class=\'boxPrecoProduto precoNormal\']/div[1]/span/text()",
    "start" : "//null",
    "description" : "//span[@id=\'textoDescricao\']/text()",
    "category" : "//h2[@class=\'titulo\']/a/text()",
    "sku" : "//span[@class=\'referencia\']/text()",
    }

    def get_meta(self):
        return self.META
