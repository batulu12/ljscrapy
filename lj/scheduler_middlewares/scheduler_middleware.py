from scrapy.core.exceptions import IgnoreRequest
from scrapy.extension import extensions
 

 
class DuplicatesFilterMiddleware(object):
    def open_domain(self, domain):
        if domain == DOMAIN:
            self.init_fingerprints()
 
    def close_domain(self, domain):
        if domain == DOMAIN:
            self.fingerprints = None
 
    def enqueue_request(self, domain, request):
        if domain != DOMAIN or request.dont_filter:
            return
        fp = self.make_fingerprint(extract_url(request.url))
        if fp in self.fingerprints:
            raise IgnoreRequest('Skipped (request already seen)')
        self.fingerprints.add(fp)
 
    def make_fingerprint(self, url):
        return hashlib.md5(url).hexdigest().upper()
 
    def init_fingerprints(self):
        self.fingerprints = set()
        mgr = extensions.enabled['MysqlManager']
        cursor = mgr.conn.execute('select recid from ljtr')
        for recid in cursor:
            self.fingerprints.add(recid)