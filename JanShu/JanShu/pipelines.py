# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class JanshuPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    """
    存如MySQL
    """
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'Jan', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """insert into article(title, author, avatar, article_id, origin_url,
                         publish_time,content) values (%s,%s,%s,%s,%s,%s,%s)"""
        self.cursor.execute(insert_sql, (item["title"], item["author"], item["avatar"], item["article_id"],
                                         item["origin_url"], item["publish_time"], item['content']))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    """
    异步存入MySQL
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        读取settings文件
        """
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted讲MySQL插入变成异步执行
        """
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        """
        处理异步插入的异常
        """
        print failure

    def do_insert(self, cursor, item):
        """
        执行具体插入
        """
        insert_sql = """insert into article(title, author, avatar, article_id, origin_url,
                                 publish_time,content, words, readers, likes, comments, rewards) 
                                 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        params = (item["title"], item["author"], item["avatar"], item["article_id"],item["origin_url"],
                  item["publish_time"], item['content'], item['words'], item['readers'], item['likes'], item['comments'], item['rewards'])
        cursor.execute(insert_sql, params)