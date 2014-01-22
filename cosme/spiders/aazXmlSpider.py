from scrapy import log
from scrapy.contrib.spiders import XMLFeedSpider
from cosme.items import CosmeItem
from scrapy.contrib.spiders import SitemapSpider
from scrapy.spider  import BaseSpider


sitemap = '/home/dev/kk_cosme/cosme/cosme/spiders/xpaths/aazsitemap.xml'
class SitemapSpider(XMLFeedSpider):

	name = 'AaBot'
	allowed_domains = ['aazperfumes.com.br']
	start_urls = ['http://www.aazperfumes.com.br/XMLProdutos.asp?IDLoja=434&Any=0&IDProduto=&IDCategoria=&RamoProd=0&PrecoDe=&PrecoAte=&Adicional1=0&Adicional2=0&Adicional3=0&SelImg=0&ExibeDescricao=0&origem=&est=1&DifName=&Mult=&Juros=&UA=False&AddParURL=&Format=0&Brand=0&Size=0']

	iterator = 'iternodes'
    	itertag = 'produto'

	def adapt_response(response):
		log.msg('Hi, this is a <%s> node!: %s')
		print ' adapt response'
		print response
	
	def parse_node(self, response, node):
		print response, node
		log.msg('Hi, this is a <%s> node!: %s' % (self.itertag, ''.join(node.extract())))

		item = Item()
		item['sku'] = node.xpath('@id_produto').extract()
		item['name'] = node.xpath('nome').extract()
		item['price'] = node.xpath('preco')
		item['description'] = node.xpath('descricao').extract()
		return item

	#def parse(self, response):
	#	print response
	#	xxs = XmlXPathSelector(response)
	#	for namespace, scheme in self.namespaces.iteritems():
	#	    xxs.register_namespace(namespace, schema)
	#	for urlnode in xxs.select('//sitemap:url'):
	#	    print urlnode
