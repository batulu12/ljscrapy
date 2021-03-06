from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.extension import ExtensionManager
from lj.items import LjItem
from lj.extensions.MysqlManager import MysqlManager
from scrapy.http import Request
from scrapy import log
import re
import hashlib
import scrapy

urldict = {}
class lj(CrawlSpider):
    name = "ljrec"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["http://bj.lianjia.com/sold/pg5905"]
    #1s  
    download_delay = 0.1
    #rules = [Rule(LinkExtractor(allow=('/sold/[^/]+.shtml')), callback = 'myparse'),
    #         Rule(LinkExtractor(allow=('/sold/[^/]', )), follow=True)]
    #def __init__(self):
    #    self.urldict = {}

    def make_url(self,page_num):
        url = "http://bj.lianjia.com/sold/pg1397"
        if page_num == 1:
            return url
        else:
            return url+'pg'+str(page_num)
            
    #def start_requests(self):
        #mgr = MysqlManager()
        #cur = mgr.conn.cursor()
        #val = cur.execute('select max(pnum) from ljdb.ljtr')
        #if val is None:
        #    page_num = 2
        #else:
        #    page_num = val
 
        # the last page may be incomplete, so we set dont_filter to be True to
        # force re-crawling it
        #return [Request(self.make_url(page_num))]
        #return [Request("http://bj.lianjia.com/sold/pg1937")]

    

    def parse(self, response):
        item = LjItem()
        x = Selector(response)
        
        sel = Selector(response)
        urls = sel.xpath("//div[@class='public paging']/ul/div/a[@class='gray_eight']/@href").extract()
        #tag = 0
        #if len(urls) != 0:
        #    tag = 1
        urls_detail = sel.xpath("//div[@class='public indetail']/div[@class='homeimg']/a/@href").extract()
        tag_wrong = sel.xpath("//div[@class='public allning']").extract()
        #if len(urls) ==0 and len(urls_detail) < 12 and len(urls_detail) > 0:
        if response.body.find('sorrynone') != -1 and len(tag_wrong) == 0:
           print "#################################"
           log.msg("#################################", level=log.WARNING)
           print response.url
           if response.url == 'http://bj.lianjia.com/sold/':
              log.msg("%%%%%%%%%%%%%%%%%", level=log.WARNING)
           yield Request(response.url, callback=self.parse, dont_filter = True)
           #f = open('C:\useful\ljscrapy\ljscrapy\lj\spiders\wrong4.html','w')
           #f.write(response.body)
           #f.close()
           

        if len(urls) == 1:
           urls_detail.append(urls[0])
        elif len(urls) == 3:
           urls_detail.append(urls[2])
        
            
        pattern = re.compile(r'http://bj.lianjia.com/sold/(\w+).shtml')
        m = pattern.match(response.url)
        if m == None:
            for url in urls_detail:   
                url = "http://bj.lianjia.com" + url 
                print url
                if url == 'http://bj.lianjia.com/sold/':
                   log.msg("**************", level=log.WARNING)                
                yield Request(url, callback=self.parse)  
            return;
        
        
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
        p = re.compile('pg(\d+)')
        list = p.findall(response.url)
        if len(list) > 0:
            item['pnum'] = list[len(list)-1]
        else:
            item['pnum'] = 1
            
        item['source'] = 'lj'
        item['remark'] = ''
        yield item
        
       
           
      