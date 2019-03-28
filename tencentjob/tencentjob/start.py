# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
from scrapy import cmdline
import os
import sys
# os模块负责程序与操作系统的交互，提供了访问操作系统底层的接口;
# sys模块负责程序与python解释器的交互，提供了一系列的函数和变量，用于操控python的运行时环境。
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
cmdline.execute(['scrapy', 'crawl', 'tencent'])
