# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request
from zhi.items import UserItem
'''
访问用户的资料接口需要在setting文件里的default_request_headers添加一个authorization属性
    DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'authorization': 'Bearer Mi4xS2NtTUF3QUFBQUFBa01JbDNSRkpEQmNBQUFCaEFsVk45ekhyV1FCbVR1QmFGR2xINjQyYkJYcEZGQ3BVWUNRajRn|1505993976|6a45a743ae225cd1428cce4a62a19d3b4b25d3a8',
}
authorization 可以通过chrome 抓包 获取这个隐藏权限赋予参数 ，可能这个值以后会改变 ，最好通过init提前获取一次确定，以后改。
抓的网址在类似这种地方 https://www.zhihu.com/people/excited-vczh/followers
将鼠标放在粉丝的头像上 查看这个时候抓到的包 你就能在requests里面发现这个参数了

不理解的地方:reboot.txt
'''
class ZhihuSpider(Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]




    '''从一个用户excited-vczh获得他的资料和他的粉丝的资料'''
    start_user = 'excited-vczh'

    '''查询单个用户信息的url'''
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'

    '''用户个人资料查询参数 包括 地址，就业，性别，教育，工作，'''
    user_query = 'locations,employments,gender,educations,business'

    '''查询用户粉丝表单的'''
    followers_url = 'https://www.zhihu.com/api/v4/members/' \
                    '{user}/followers?include={include}&offset={offset}&limit={limit}'

    '''用于查询一个人的粉丝信息的参数 '''
    followers_query = 'answer_count,articles_count'


    '''从excited-vczh用户开始爬取'''
    def start_requests(self):
        '''返回到parse_user获取用户详细资料 '''
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)

    '''获取用户详细资料'''
    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()

        try:

            url_token = result['url_token']
            gender = result['gender']
            headline = result['headline']

            '''???我也不想这么写啊  我。。。暂时没想到什么好办法 写if else太痛苦 写默认值 里面还有列表 ？？？？'''
            try:
                business_name = result['business']['name']
            except Exception:
                business_name = 'None'

            try:
                location_name = result['locations'][0]['name']
            except Exception:
                location_name = 'None'

            try:
                school_name = result['educations'][0]['school']['name']
            except Exception:
                school_name = 'None'

            try:
                employments_job_name = result['employments'][0]['job']['name']
            except Exception:
                employments_job_name = 'None'

            try:
                employments_company_name = result['employments'][0]['company']['name']
            except Exception:
                employments_company_name='None'

            item['url_token'] = url_token
            item['business_name'] = business_name
            item['location_name'] = location_name
            item['school_name'] = school_name
            item['gender'] = gender
            item['headline'] = headline
            item['employments_job_name'] = employments_job_name
            item['employments_company_name'] = employments_company_name
            yield item
        except Exception,e:
            print "用户资料不完全"

        '''根据用户名字 获取他的粉丝列表'''
        yield Request(
            self.followers_url.format(user=result.get('url_token'), include=self.followers_query, limit=20, offset=0),
            self.parse_followers)

    '''根据用户的粉丝列表 获取下一页粉丝列表 并且把当前粉丝列表每一个用户的url_token传输给parser_user函数，获得用户的详细资料'''
    def parse_followers(self, response):
        results = json.loads(response.text)


        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,
                          self.parse_followers)