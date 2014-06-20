import logging

#BOT_NAME = 'cosme'
#BOT_VERSION = '1.0'

#Guerilla warfare!

BOT_NAME = 'HOSS'

ITEM_PIPELINES = ['fixedcrawler.Hoss_pipeline']
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
