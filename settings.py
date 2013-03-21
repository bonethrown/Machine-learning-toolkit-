# Scrapy settings for cosme project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

#BOT_NAME = 'cosme'
#BOT_VERSION = '1.0'

#Guerilla warfare!

BOT_NAME = 'Mozilla'
BOT_VERSION = '5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0a2) Gecko/20111101 Firefox/9.0a2'

ITEM_PIPELINES = ['cosme.pipelines.CosmePipeline']
SPIDER_MODULES = ['cosme.spiders']
NEWSPIDER_MODULE = 'cosme.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DOWNLOAD_DELAY = 0


HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = "HTTP_CACHE"
HTTPCACHE_STORAGE = "scrapy.contrib.downloadermiddleware.httpcache.FilesystemCacheStorage"

