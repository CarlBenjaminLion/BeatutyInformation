# coding=utf-8
'''
本脚本用来抓取美容人才网
http://www.138job.com
的所有关于美容行业的公司信息，职位信息
并且整理成字典，导出json文件
网页爬取流程
登陆，伪装浏览器
抓取职业的基础URL，处理成 RenCaiWang 对象
通过RenCaiWang对象来抓取公司页面的URL，并
'''
import urllib
import json
import re
import bs4


if __name__ == '__main__':
    pass

