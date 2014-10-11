# Scrapy settings for test project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'lj'

SPIDER_MODULES = ['lj.spiders']
NEWSPIDER_MODULE = 'lj.spiders'
ITEM_PIPELINES = ['lj.pipelines.LjPipeline']

SCHEDULER_MIDDLEWARES = {
    'crawl.scheduler_middlewares.DuplicatesFilterMiddleware': 500
}


HOST='localhost'
USER='root'
PASSWD='hshy12'
CHARSET='utf8'
PORT = 3306

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'C://useful//ljscrapy//ljscrapy//lj//log//lj.log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test (+http://www.yourdomain.com)'