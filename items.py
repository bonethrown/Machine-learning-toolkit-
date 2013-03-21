# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CosmeItem(Item):
    # define the fields for your item here like:
     name = Field()
     brand = Field()
     sku = Field()
     image = Field()
     price = Field()
     category = Field()
     description = Field()
     stars = Field()
     site = Field()
     url = Field()
     date_crawled = Field()
     pass
