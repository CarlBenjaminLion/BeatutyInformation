# coding=utf-8
import requests

ip_proxy = '116.208.66.37:53281'
r = requests.get('http://www.baidu.com/', proxies = {'http':ip_proxy}, timeout=3)
if r.status_code == 200:
    print('success')