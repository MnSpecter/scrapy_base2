SPIDER_MODULES = ['jobparser.spiders']
NEWSPIDER_MODULE = 'jobparser.spiders'
USER_AGENT = 'Mozilla/5.0'
ROBOTSTXT_OBEY = False
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'  #INFO ERROR
LOG_FILE = 'log.txt'
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8
IMAGES_STORE = 'images'
ITEM_PIPELINES = {
   'jobparser.pipeline.DataBasePipeline': 300,
   'jobparser.pipeline.PhotosPipeline': 200,
}

