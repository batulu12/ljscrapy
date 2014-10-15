#-*- coding:UTF-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import sys
import MySQLdb
from scrapy.extension import ExtensionManager
from lj.extensions.MysqlManager import MysqlManager


class LjPipeline(object):
    
    #def __init__(self):
        #self.hashque = 
        
    def process_item(self, item, spider):
        reload(sys)
        sys.setdefaultencoding( "utf-8" )        
        #print item['title']
        #print item['price']
        #print item['date']
        #print item['des'].encode('GB18030')
        #print item['duration']
        #print item['floor'] 
        #print item['recid']
        #print item['region']
        #print item['detail_region']
        #print item['community']
        
        ###########################################################/
        try:
            #conn = MySQLdb.connect(host='localhost',user='root',passwd='hshy12',charset='utf8',port = 3306)
            #cur = conn.cursor()
            mgr = MysqlManager()
            cur = mgr.conn.cursor()
            #cur  = extensions.enabled['MysqlManager']
            #value = [item['recid'],item['title']]
            value = []
            value.append(item['recid'])
            value.append(item['title'])
            value.append(item['price'])
            value.append(item['date'])
            value.append(item['floor'])
            value.append(item['duration'])         
            value.append(item['des'])
            value.append(item['url'])
            value.append(item['source'])
            value.append(item['remark'])  
            value.append(item['region'])
            value.append(item['detail_region'])
            value.append(item['community'])
            value.append(item['pnum'])
            cur.execute('insert into ljdb.ljtr values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
            mgr.conn.commit()
            cur.close()
            mgr.conn.close()
            #conn.commit()
            #cur.close()
            #conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d:%s" % (e.args[0],e.args[1])
            
            
            
            #################################################################/
        #print item['title']
        #print item['region']
        #print item['detail_region']
        #print item['community']
        #print item['price']
        #print item['builtarea']
        #t = u'汉'
        #print t
        
        #line ='{'
        #for (d,x) in item.items():
            #temp = d.encode('GB18030')+":"+str(x).encode('GB18030')
            #line = line + temp +' , '
            
        #line = line +'}\n'
        #print line
        #self.file.write(line)
        return item
