from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from lj.items import LjItem

class lj(CrawlSpider):
    name = "lj"
    allowed_domains = ["beijing.homelink.com.cn"]
    start_urls = ["http://beijing.homelink.com.cn/ershoufang/BJHD86983254.shtml",
                  "http://beijing.homelink.com.cn/ershoufang/pg2"]
    rules = [Rule(SgmlLinkExtractor(allow=('/ershoufang/[^/]+.shtml')), callback = 'myparse'),
             Rule(SgmlLinkExtractor(allow=('/ershoufang/pg[^/]', )), follow=True)]
    def myparse(self, response):
        item = LjItem()
        x = HtmlXPathSelector(response)
        item['url'] = response.url
        strlist = x.xpath('//h1/text()').extract()
        if len(strlist) > 0:
            item['title'] = strlist[0]
        else:
            item['title'] = 'hello'
           
        strlist = x.xpath("//div[contains(@class,'public nav')]/a/text()").extract()
        if len(strlist) > 0:
            item['region'] = strlist[2]
        else:
            item['region'] = 'region'
            
        if len(strlist) > 0:
            item['detail_region'] = strlist[3]
        else:
            item['detail_region'] = 'detail_region'
            
        if len(strlist) > 0:
            item['community'] = strlist[4]
        else:
            item['community'] = 'community'        
            
        strlist = x.xpath("//div[@class='shoujia']/ul/li/span/text()").extract()
        
        if len(strlist) > 0:
            item['price'] = strlist[0]
        
        strlist = x.xpath("//div[@class='shoujia']/ul/li/div[@class='reduce']/div[@class='prompt']/text()").extract()
        
        if len(strlist) > 0:
            item['trend'] = strlist[0]
            
        strlist = x.xpath("//div[@class='shoujia']/ul/li[4]/text()").extract()
        
        if len(strlist) > 0:
            item['builtarea'] = strlist[0]        
            
        return item