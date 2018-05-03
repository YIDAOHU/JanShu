# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    origin_url = scrapy.Field()
    author = scrapy.Field()
    avatar = scrapy.Field()
    publish_time = scrapy.Field()
    readers = scrapy.Field()
    likes = scrapy.Field()
    words = scrapy.Field()
    comments = scrapy.Field()
    rewards = scrapy.Field()

