# -*- coding: utf-8 -*-
import scrapy
import tencentjob.items


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    baseurl = "https://hr.tencent.com/"
    offset = 0

    def start_requests(self):
        while self.offset < 10:
            url = "https://hr.tencent.com/position.php?keywords=&tid=0&lid=2175&start="+str(self.offset*10)+"#a"
            yield scrapy.Request(url, headers=self.headers)
            self.offset += 1

    def parse(self, response):
        urllist = response.css("table tr td.l.square a::attr(href)")
        for urlline in urllist:
            pageurl = self.baseurl+urlline.extract()
            yield scrapy.Request(pageurl, headers=self.headers, callback=self.page_parse)

    def page_parse(self, response):
        title = response.css('#sharetitle::text').extract_first("")
        workplace = response.css('table tr.c.bottomline td:nth-child(1)::text').extract_first("")
        position = response.css('table tr.c.bottomline td:nth-child(2)::text').extract_first("")
        zpnum = response.css('table tr.c.bottomline td:nth-child(3)::text').extract_first("")
        duty_of_worklist = response.css('table tr td ul li::text').extract()
        workinfo = "".join(duty_of_worklist)
        tencentitem = tencentjob.items.TencentjobItem()
        tencentitem['title'] = title
        tencentitem['workplace'] = workplace
        tencentitem['position'] = position
        tencentitem['zpnum'] = zpnum
        tencentitem['workinfo'] = workinfo
        yield tencentitem

