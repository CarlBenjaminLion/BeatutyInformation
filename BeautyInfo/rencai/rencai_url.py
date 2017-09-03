# coding=utf-8
from urllib.request import *
from bs4 import BeautifulSoup
import chardet
import requests
import re
from multiprocessing import Pool


class RenCai(object):
    def __init__(self):
        self.root_url = 'http://www.138job.com/'
        self.search_url = 'http://s.138job.com/hire/%d?keyword=&workadd=0&keywordtype=1&position=%d'
        self.search_url_1 = 'http://s.138job.com/hire/'
        self.search_url_2 = '?keyword=&workadd=0&keywordtype=1&position='
        self.new_position_list_urls = []
        self.old_position_list_urls = []
        self.new_position_urls = []
        self.old_position_urls = []
        self.headers = [
            {'Use-Agent': "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"},
            {"Use-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"},
            {"Use-Agent": "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10"},
            {"Use-Agent": "Opera/8.0 (Windows NT 5.1; U; en)"},
            {"Use-Agent": "Openwave/ UCWEB7.0.2.37/28/999"},
            {"Use-Agent": "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"},
            {"Use-Agent": "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"},
            {"Use-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16"},
        ]


    def decode_html(self, html):
        pass
        html_text = html.decode(chardet.detect(html)['encoding'], 'ignore')
        return html_text

    def get_html_txt(self, page_url):
        try:
            # print('begin')
            html = urlopen(page_url).read()
            # print(html)
            html_txt = self.decode_html(html)
            # print(html_txt)

        except:
            return None
        return html_txt

    def get_bs_obj(self, html_txt):
        try:
            if html_txt is None or html_txt == '':
                return None
            else:
                bs_obj = BeautifulSoup(html_txt, 'html.parser')
        except:
            print('===============解析BS对象失败===============')
            return None
        return bs_obj

    def get_position_page(self, i):
        url_list = []
        try:
            for j in range(1, 150):
                url = self.search_url_1 + str(j) + self.search_url_2 + str(i)
                print(url)
                html_txt = self.get_html_txt(url)
                bs_obj = self.get_bs_obj(html_txt)
                weiye = bs_obj.find_all('div', class_='pager')
                if weiye == []:
                    return
                self.new_position_list_urls.append(url)
                url_file = open('url_file.txt', 'a')
                url_file.write(url + '\n')
                url_file.close()

        except:
            print('+++++++++++++++++访问和解析页面失败了++++++++++++++++++++')



        return self.new_position_list_urls

class ProxyIp(object):

    def __init__(self):
        self.proxy_url = 'http://www.xicidaili.com/nn/'
        self.proxy_ip = []

    def decode_html(self, html):
        pass
        html_text = html.decode(chardet.detect(html)['encoding'], 'ignore')
        return html_text

    def get_proxy_ip(self):
        req = Request(self.proxy_url)
        req.add_header("User-Agent","Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.")
        html = urlopen(req).read()
        html_txt = self.decode_html(html)
        bs_obj = BeautifulSoup(html_txt, 'html.parser')
        # print(html_txt)
        ip_list_nodes = bs_obj.find_all('tr', class_='odd')
        print(ip_list_nodes)


if __name__ == '__main__':
    # obj = RenCai()
    # obj.get_position_page(4)
    obj = ProxyIp()
    obj.get_proxy_ip()