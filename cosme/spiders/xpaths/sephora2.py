from cosme.spiders.xpaths.abstract_xpath import AbstractXPath

class Sephora2XPath(AbstractXPath):
    META = {
    
    "image" : "//div[@class=\'lateralImagemProduto highslide-gallery\']/img/@src",
    "name" :  "//div[@class=\'tituloDescricaoProduto\']/h1/text()",
    "brand" : "//ul[@class=\'breadCrumb\']/li[1]/a/text()",
    "price" : "//td[@class=\'precoSKU\']/div/span[@class=\'produtoPrecoVendaPor\']/text()",
    "description" : "//div[@class=\'descricaoProduto\']/p/text()",
    "category" : "//ul[@class=\'breadCrumb\']/li[4]/a/text()",
    "sku" : "//td[@class=\'refSKU\']/span[@class=\'refSKUNumero\']/text()"
    }
    
    COMMENTS = {
       "commentList":  "//ul[@class=\'produtoListaComentarios\']/li",
       "commenterName": ".//h3/span/text()",
       "commentText": ".//p/text()",
       "commentDate": ".//h3/text()",
       "commentStar": ".//div[contains(@class, 'avaliacaoProduto')]/@class"
    }

    def get_meta(self):
        return self.META
    
    
    def get_comments(self):
        return self.COMMENTS