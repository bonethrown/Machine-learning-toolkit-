from cosme.spiders.xpaths.abstract_xpath import AbstractXPath
class BelezanaWebXPath(AbstractXPath):
    
    META = {
            "image" : "//img[@id=\'imagem4\']/@src",
    
            "name" :  "//div[@class='dados_topo_produto']/h1[@class='title-product']/text()",
    
            "brand" : "//div[@class='topo_produto']/div[@class='marca_produto']/a/img/@title",
    
            "price" : "//li[@class='preco-promocao']",
    
            "description" : "//div[@id='aba-descricao']/div[@itemprop='description']",
    
            "category" : "//div[@id='aside']/div[1]/ul[@class='breadcrumbs']/li[2]/a/span/text()" ,
    
            "sku" : "//div[@class=\'title\']/p/text()" ,
            
            "comments":  "//div[@class=\"rateAndTips\"]",

	    "volume" : "//div[@class='prices']/div[1]",
            }
    
    def get_meta(self):
        return self.META

    COMMENTS = {
       "commentList":  "//div[@class=\"rate\" or @class=\"mainRate\"]",
       "commenterName": ".//div[@class=\'content\']/div[@class=\'stars\']/span[2]/text()",
       "commenterName2": ".//div[@class=\'stars\']/span[2]/text()",
       "commentText": ".//div[@class=\'content\']/div[@class=\'text\']/div/p/text()",
       "commentText2": ".//div[@class=\'text\']/div/p/text()",
       "commentDate": ".//li[@id=\'star\']/div[@class=\'dados\']/text()",
       "commentStar": ".//div[@class=\'content\']/div[@class=\'stars\']/span/img",
       "commentStar2": ".//div[@class=\'stars\']/span/img"
    }
    def get_price_multi(self):
	return "//@data-value"
    
    def get_comments(self):
        return self.COMMENTS
