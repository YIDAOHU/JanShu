# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse
import time


class JSPageMiddleware(object):
    """
    通过浏览器请求动态网页
    """
    def process_request(self, request, spider):
        if spider.name == "janshu":
            spider.browser.get(request.url)
            time.sleep(1)

            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                encoding='utf8', request=request)
