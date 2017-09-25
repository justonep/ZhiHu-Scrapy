# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ZhiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    answerList = scrapy.Field()

class UserItem(scrapy.Item):
    # define the fields for your item here like:
    url_token = Field()
    business_name = Field()
    location_name = Field()
    school_name = Field()
    gender = Field()
    employments_job_name = Field()
    employments_company_name = Field()
    headline=Field()
