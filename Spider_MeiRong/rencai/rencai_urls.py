# coding=utf-8
from urllib.request import *
from bs4 import BeautifulSoup
import chardet
import requests
import re
from multiprocessing import Pool
import time
import rencai_urlopen


def decode_html(html):
    pass
    html_text = html.decode(chardet.detect(html)['encoding'], 'ignore')
    return html_text


class RequestRenCai(object):
    def __init__(self):
        self.root_url = 'http://www.138job.com/'
        self.search_url = 'http://s.138job.com/hire/%d?keyword=&workadd=0&keywordtype=1&position=%d'
        self.search_url_1 = 'http://s.138job.com/hire/'
        self.search_url_2 = '?keyword=&workadd=0&keywordtype=1&position='
        self.new_position_list_urls = []
        self.old_position_list_urls = []
        self.new_position_urls = []
        self.old_position_urls = []

    def get_html_txt(self, page_url):
        html = urlopen(page_url, timeout=5).read()
        html_txt = decode_html(html)
        time.sleep(0.5)
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
        try:
            for j in range(1, 150):
                url = self.search_url_1 + str(j) + self.search_url_2 + str(i)
                print('=========== '+url+' ===========')
                file = open('duandian.txt', 'w')
                file.write(url)
                file.close()
                html_txt = self.get_html_txt(url)
                bs_obj = self.get_bs_obj(html_txt)
                weiye = bs_obj.find_all('div', class_='pager')
                # print(weiye)
                if weiye == []:
                    return
                else:
                    self.get_urls_from_list_page(url)
        except:
            print('+++++++++++++++++访问和解析页面失败了++++++++++++++++++++')
        # print(self.new_position_urls)

    def get_urls_from_list_page(self, list_page):
        # 传入一个职位列表Url，然后从此解析职位页面Url，然后抽取信息
        # list_page = 'http://s.138job.com/hire/1?keyword=&workadd=0&keywordtype=1&position=2212'
        html_txt = self.get_html_txt(list_page)
        bs_obj = self.get_bs_obj(html_txt)
        if bs_obj == None:
            print("-----------解析职位列表信息页面失败------------")
            return
        else:
            positon_list = bs_obj.find_all('a', href=re.compile('.*H.*'))
            for i in positon_list:
                self.new_position_urls.append(i['href'])
                # print(self.new_position_urls)



    def main(self, i):
        self.get_position_page(i)



if __name__ == '__main__':
    obj_urls = RequestRenCai()
    for i in range(1003, 2500):
        try:
            print(i)
            # obj_urls.get_position_page(i)
            obj_urls.main(i)
            for num in range(len(obj_urls.new_position_urls)):
                try:
                    url = obj_urls.new_position_urls.pop()
                    obj_open = rencai_urlopen.RenCaiGetData(url)
                    obj_open.open()
                except:
                    pass

        except:
            pass