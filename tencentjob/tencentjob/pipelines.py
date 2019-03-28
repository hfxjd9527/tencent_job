# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class TencentjobPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        self.db = self.client['tecent_job']

    def process_item(self, item, spider):
        data = dict(item)
        self.db['tencent'].insert(data)
        return item
