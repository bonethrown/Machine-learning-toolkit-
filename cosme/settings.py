# Scrapy settings for cosme project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import logging

#BOT_NAME = 'cosme'
#BOT_VERSION = '1.0'

#Guerilla warfare!

BOT_NAME = 'Mozilla'

ITEM_PIPELINES = ['cosme.pipelines.CosmePipeline']
SPIDER_MODULES = ['cosme.spiders']
NEWSPIDER_MODULE = 'cosme.spiders'
USER_AGENT = '%s' % (BOT_NAME)
DOWNLOAD_DELAY = 3

DEPTH_LIMIT=0

#CLOSESPIDER_PAGECOUNT=5

RANDOMIZE_DOWNLOAD_DELAY=True
DOWNLOAD_DELAY = 0.45  

# Debug is Very noisy.
LOG_LEVEL='INFO'

#analytics
EXTENSIONS = {'cosme.extensions.Analytics.Analytics':500}
ANALYTICS_ENABLED = True


#email
MAIL_HOST = 'smtp.live.com' 
MAIL_FROM = 'alptilev@hotmail.com'
MAIL_USER = 'alptilev@hotmail.com'
MAIL_PASS = 'Naberulan2'
MAIL_PORT = 587
MAIL_SSL = True

COSME_DEBUG=True

HTTP_NUMPOOLS=2
HTTP_MAXSIZE=10

logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s %(levelname)s %(name)s:%(lineno)s  %(message)s',
)
