# coding=utf-8
'''
测试脚本，来测试recai这一个包的使用是否正常，功能是否满足需要
'''
import requests
from urllib.request import *
def open_url_requests():
    url = 'http://s.138job.com/hire/14?keyword=&workadd=0&keywordtype=1&position=1000'
    proxy = {'http' : '116.16.105.137:9000'}
    proxy_support = ProxyHandler(proxy)
    opener = build_opener(proxy_support)

    install_opener(opener)
    response = urlopen(url, timeout=20)
    html = response.read()
    print(html)


if __name__ == '__main__':
    open_url_requests()