# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
import requests
from scrapy.selector import Selector
import pymongo


class Tencentjob:
    baseurl = "https://hr.tencent.com/"
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client['tencentjob']

    def get_data(self, url):
        # 返回经过Selector解析过得页面数据
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        res = requests.get(url, headers=headers)
        data = Selector(res)
        return data

    def get_pageinfo(self, data):
        # 返回每个页面的招聘信息
        urllist = data.css("table tr td.l.square a::attr(href)")
        for urlline in urllist:
            url = urlline.extract()
            pageurl = self.baseurl + url
            pagedata = self.get_data(pageurl)
            title = pagedata.css('#sharetitle::text').extract_first("")
            workplace = pagedata.css('table tr.c.bottomline td:nth-child(1)::text').extract_first("")
            position = pagedata.css('table tr.c.bottomline td:nth-child(2)::text').extract_first("")
            zpnum = pagedata.css('table tr.c.bottomline td:nth-child(3)::text').extract_first("")
            duty_of_worklist = pagedata.css('table tr td ul li::text').extract()
            workinfo = "".join(duty_of_worklist)
            result = {
                "url": pageurl,
                "title": title,
                "workplace": workplace,
                "position": position,
                "zpnum": zpnum,
                "workinfo": workinfo,
            }
            if result:
                self.save_to_mongo(result)

    def save_to_mongo(self, result):
        if self.db['tencentjob'].insert(result):
            print("save to mongodb success", result)


if __name__ == '__main__':
    t = Tencentjob()
    for i in range(10):
        indexurl = "https://hr.tencent.com/position.php?keywords=&tid=0&lid=2175&start="+str(i*10)+"#a"
        data = t.get_data(indexurl)
        t.get_pageinfo(data)