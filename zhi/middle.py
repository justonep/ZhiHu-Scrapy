from selenium import webdriver
from scrapy.http import HtmlResponse
class WebkitDownloaderTest(object):
    def process_request(self,request,spider):
        driver=webdriver.PhantomJS(executable_path='/scrapy/phantomjs/bin/phantomjs')
        driver.get(request.url)
        content=driver.page_source.encode('utf-8')
        return HtmlResponse(request.url,body=content)