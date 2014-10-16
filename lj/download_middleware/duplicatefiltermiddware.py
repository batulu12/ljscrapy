from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request
from lj.extensions.MysqlManager import MysqlManager
import hashlib
 

 
class DuplicatesFilterMiddleware(object):
    def __init__(self):
        self.fingerprints = None
        
    def init_fingerprints(self):
        self.fingerprints = set()
        mgr = MysqlManager()
        cur = mgr.conn.cursor()
        cur.execute('select recid from ljdb.ljtr')
        results = cur.fetchall()
        for recid in results:
            self.fingerprints.add(recid[0])
            
    def process_request(self,request, spider):
        if self.fingerprints == None:
           self.init_fingerprints()        
        self.enqueue_request(request)
 
    def enqueue_request(self,request):
    
        fp = self.make_fingerprint(request.url)
        if fp in self.fingerprints:
            raise IgnoreRequest('Skipped (request already seen)')
           
        self.fingerprints.add(fp)
 
    def make_fingerprint(self, url):
        return hashlib.md5(url).hexdigest().upper()
 
    