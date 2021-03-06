#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: tencentjob

from pyspider.libs.base_handler import *
import pymongo

class Handler(BaseHandler):
    crawl_config = {
    }
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client['pytencentjob']
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://hr.tencent.com/position.php?keywords=&tid=0&lid=2175&start=0#a', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('table tr td.l.square a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        result = {
            "url": response.url,
            "title": response.doc('#sharetitle').text(),
            "workplace": response.doc('table tr.c.bottomline td:nth-child(1)').text(),
            "position": response.doc('table tr.c.bottomline td:nth-child(2)').text(),
            "zpnum": response.doc('table tr.c.bottomline td:nth-child(3)').text(),
            "duty_of_work": response.doc('table tr td ul li').text(),
        }
        if result:
            self.save_to_mongo(result)
    def save_to_mongo(self, result):
        if self.db['tencentjob'].insert(result):
            print("Yeah,I can do it", result)
    
