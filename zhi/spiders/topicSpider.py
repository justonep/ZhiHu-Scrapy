# -*- coding: utf-8 -*-
import scrapy
from zhi.items import ZhiItem
class LoginPySpider(scrapy.Spider):
    name = 'topic'

    webheader = {
    # 'Accept': 'text/html, application/xhtml+xml, */*',
    # 'Accept-Language': 'zh-CN',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
    # 'User-Agent': 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    # 'DNT': '1',
    # 'Connection': 'Keep-Alive'
    }

    cookies={}

    def start_requests(self):
        requestList=[]
        # wide = 10
        for i in range(1, 11):
            req=scrapy.http.Request(
                url='https://www.zhihu.com/topic/19554300/top-answers?page='+str(i),
                headers=self.webheader,
                cookies=self.cookies,
                callback=self.parse_topic,
                dont_filter=True,)
            yield req
    
    def parse_topic(self, response):
        questionList=response.xpath('//*[@id="zh-topic-top-page-list"]/div')
        for questionItem in questionList:
            questionUrl=questionItem.xpath('div/div/h2/a/@href').extract()[0]
            print(questionUrl)
            req=scrapy.http.Request(
                url='https://www.zhihu.com'+questionUrl,
                headers=self.webheader,
                cookies=self.cookies,
                callback=self.parse_one_page,
                dont_filter=True,)
            yield req

    def parse_one_page(self,response):
        title=response.xpath('//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div[1]/h1/text()').extract()[0]

        '''print(title)'''

        answerList=response.xpath('// *[ @ id = "QuestionAnswers-answers"]/div[1]/div/div[2]/div/div/div[2]/div[1]/span').extract()

        sum=ZhiItem()
        sum['title']=title
        sum['answerList']=answerList
        yield sum


