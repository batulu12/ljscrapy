# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LjItem(Item):
    # define the fields for your item here like:
    # name = Field()
    url = Field()
    title = Field()
    region = Field()
    detail_region = Field()
    community = Field()
    price = Field()
    unit_price = Field()
    trend = Field()
    builtarea = Field()
    floor = Field()
    des = Field()
    duration = Field()
    date = Field()
    recid = Field()
    source = Field()
    remark = Field()
    pnum = Field()
    pass
