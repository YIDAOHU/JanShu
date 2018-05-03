# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from JanShu.items import ArticleItem
from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from JanShu.common import extract_num


class JanshuSpider(CrawlSpider):
    name = 'janshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_item', follow=True),
    )

    def __init__(self):
        self.browser = webdriver.PhantomJS()
        super(JanshuSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 当爬虫退出时关闭浏览器
        print("spider closed")
        self.browser.quit()

    def parse_item(self, response):
        # 文章标题
        title = response.xpath('//h1[@class="title"]/text()').get()
        # 用户图像
        avatar = response.xpath('//a[@class="avatar"]/img/@src').get()
        # 作者
        author = response.xpath('//span[@class="name"]/a/text()').get()
        # 发表时间
        publish_time = response.xpath('//span[@class="publish-time"]/text()').get()
        origin_url = response.url
        # 文章id
        article_id = response.url.split('?')[0].split('/')[-1]
        # 文章内容
        content = response.xpath('//div[@class="show-content"]').get()
        # 字数
        words = extract_num(response.xpath('//span[@class="wordage"]/text()').get())
        # 阅读数
        readers = extract_num(response.xpath('//span[@class="views-count"]/text()').get())
        # 评论数
        comments = extract_num(response.xpath('//span[@class="comments-count"]/text()').get())
        # 喜欢人数
        likes = extract_num(response.xpath('//span[@class="likes-count"]/text()').get())
        # 赞赏人数
        rewards = extract_num(response.xpath('//span[@class="rewards-count "]/text()').get()
                              )

        item = ArticleItem(title=title, author=author, avatar=avatar, origin_url=origin_url, content=content,
                           publish_time=publish_time, article_id=article_id, words=words, readers=readers,
                           comments=comments, likes=likes, rewards=rewards)

        yield item
