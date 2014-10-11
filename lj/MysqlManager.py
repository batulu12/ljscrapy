import MySQLdb
from os import path
 
from scrapy.conf import settings
from scrapy.core import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.core.exceptions import NotConfigured
 
class MysqlManager(object):
    def __init__(self):
        if settings.get('HOST') is None:
            raise NotConfigured
 
        self.conn = None
        self.initialize()
        dispatcher.connect(self.finalize, signals.engine_stopped)
 
    def initialize(self):
        host = settings['HOST']
		user = settings['USER']
		passwd = settings['PASSWD']
		charset = settings['CHARSET']
		port = settings['PORT']
		self.conn = MySQLdb.connect(host,user=,passwd,charset,port)
        
 
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
