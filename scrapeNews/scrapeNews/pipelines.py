# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
from scrapeNews.items import ScrapenewsItem
import envConfig

# Setting up local variables USERNAME & PASSWORD
PASSWORD = envConfig.PASSWORD
USERNAME = envConfig.USERNAME

class ScrapenewsPipeline(object):

    def open_spider(self, spider):
        self.connection = psycopg2.connect(host='localhost', user=USERNAME, database='scraped_news', password=PASSWORD)
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True


    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()


    def process_item(self, item, spider):
        self.cursor.execute("""SELECT link from news_table where site_id = %s and link= %s """, (item.get('source'), item.get('link')))
        if not self.cursor.fetchall():
            try:
                self.cursor.execute("""INSERT INTO news_table (title, content, image, link, newsDate, site_id) VALUES (%s, %s, %s, %s, %s, %s)""" , (item.get('title'), item.get('content'), item.get('image'), item.get('link'), item.get('newsDate'), item.get('source')))
                self.connection.commit()
            except Exception as Error:
                print ("Error 103: ", Error)
            finally:
                return item
        else:
            return item
