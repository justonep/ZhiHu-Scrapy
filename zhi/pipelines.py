# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class ZhiPipeline(object):
    def process_item(self, item, spider):
        conn = MySQLdb.connect(host="192.168.0.179",user="root",passwd="123123",db='sanle',charset="utf8")
        cursor = conn.cursor()
        try:
            cursor.execute("insert into title(title) values('%s')" % (item['title']) )
            id=int(conn.insert_id())
            conn.commit()
        except Exception as e:
            print(e)

        try:
            for answer in item['answerList']:
                cursor.execute("insert into answer(answer,title_id) values('%s','%s')" % (answer,id))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()
        return item

class UserInfo(object):
    def process_item(self,item,spider):
        conn = MySQLdb.connect(host="192.168.0.179",user="root",passwd="123123",db='sanle',charset="utf8")
        cursor=conn.cursor()
        cursor.execute("insert into zhihuUserInfo (url_token,business_name,location_name,school_name,gender,employments_job_name,employments_company_name,headline) values('%s','%s','%s','%s','%s','%s','%s','%s') "
                           % (item['url_token'],item['business_name'],item['location_name'],item['school_name'],
                            item['gender'],item['employments_job_name'],item['employments_company_name'],item['headline']))
        conn.commit()
