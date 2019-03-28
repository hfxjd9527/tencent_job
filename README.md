# tencent_job
使用简单代码、scrapy框架、pyspider三种方式抓取腾讯招聘信息，并保存到MongoDB数据库
使用css选择器对页面进行定位，使代码可以在简单代码、scrapy、pyspider中复用。scrapy重写了start_requests，
加入了user-agent。
也可以修改middlewares，引用fake_useragent来实现同样的功能，只是简单爬虫，似乎不必小题大做。如遇复杂的网页，可以尝试。
