from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from lj.items import LjItem
import hashlib

urldict = {}
class lj(CrawlSpider):
    name = "ljrec"
    allowed_domains = ["beijing.homelink.com.cn"]
    start_urls = ["http://beijing.homelink.com.cn/sold/d2b75/"]
    rules = [Rule(SgmlLinkExtractor(allow=('/sold/[^/]+.shtml')), callback = 'myparse'),
             Rule(SgmlLinkExtractor(allow=('/sold/[^/]', )), follow=True)]
    #def __init__(self):
    #    self.urldict = {}

    def myparse(self, response):
        item = LjItem()
        x = HtmlXPathSelector(response)
        urlmd5 = hashlib.md5(response.url).hexdigest().upper()
        if not urldict.has_key(urlmd5):
            urldict[urlmd5] = 0
            item['recid'] = urlmd5
        else:
            item['recid'] = 'null'
            pass 
        item['url'] = response.url
        strlist = x.xpath('//title/text()').extract()
        if len(strlist) > 0:
            item['title'] = strlist[0]
        else:
            item['title'] = 'null'
            
        strlist = x.xpath("//div[@class='public allning']/a/text()").extract()
        
        if len(strlist) > 4:
            item['region'] = strlist[2]
            item['detail_region'] = strlist[3]
            item['community'] = strlist[4]
        else:
            item['region'] = 'null'
            item['detail_region'] = 'null'
            item['community'] = 'null'           
            
        strlist = x.xpath("//div[@class='public conjuncture']/div[@class='nring']/ul/li/span[@class='red']/text()").extract()    
        if len(strlist) > 0:
            item['price'] = strlist[0]
        else:
            item['price'] = 'null'
            
        strlist = x.xpath("//div[@class='public conjuncture']/div[@class='nring']/ul/li/span[@class='one']/text()").extract()    
        if len(strlist) > 0:
            item['date'] = strlist[0]
        else:
            item['date'] = 'null'        
            
        strlist = x.xpath("//div[@class='yilianxu']/p/kbd/text()").extract()
        
        if len(strlist) > 0:
            item['des'] = strlist[0]
        else: 
            item['des'] = 'null'
        
        strlist = x.xpath("//div[@class='yilianxu']/ul/li/span[@class='red']/text()").extract()
        
        if len(strlist) > 0:
            item['duration'] = strlist[0]
        else:
            item['duration'] = 'null'
            
        strlist = x.xpath("//div[@class='yilianxu']/p/text()").extract()
        
        if len(strlist) > 0:
            item['floor'] = strlist[0] 
        else:
            item['floor'] = 'null'
        item['url'] = response.url
        item['source'] = 'lj'
        item['remark'] = ''
        return item