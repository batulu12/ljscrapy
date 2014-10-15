import MySQLdb
from os import path
 
from scrapy import signals
from scrapy.exceptions import NotConfigured
 
class MysqlManager(object):
    def __init__(self):
        #if settings.get('HOST') is None:
        #    raise NotConfigured
 
        self.conn = None
        self.host = None
        self.user = None
        self.passwd = None
        self.charset = None
        self.port = None
        self.initialize()
        #dispatcher.connect(self.finalize, signals.engine_stopped)
        
    @classmethod    
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.get('HOST'):
            raise NotConfigured
        
        host = crawler.settings.get('HOST')
        user = crawler.settings.get('USER')
        passwd = crawler.settings.get('PASSWD')
        charset = crawler.settings.get('CHARSET')
        port = crawler.settings.get('PORT')
        # instantiate the extension object
        ext = cls()
        # connect the extension object to signals
        crawler.signals.connect(ext.initialize, signal=signals.spider_opened)
        crawler.signals.connect(ext.finalize, signal=signals.engine_stopped)
        # return the extension object
        return ext
 
    def initialize(self):
        #host = settings['HOST']
        #user = settings['USER']
        #passwd = settings['PASSWD']
        #charset = settings['CHARSET']
        #port = settings['PORT']
        #self.conn = MySQLdb.connect(host,user,passwd,charset,port)
        #print host
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='hshy12',charset='utf8',port = 3306)
        
 
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
