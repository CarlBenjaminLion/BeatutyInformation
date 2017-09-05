# coding=utf-8
from urllib.request import *
from bs4 import BeautifulSoup
import chardet
import requests
import re
from multiprocessing import Pool
import time
from rencai_parse import *


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
        # self.proxy_ip = ['222.34.139.52:808']
        #self.headers = [
        #    {'Use-Agent': "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"},
        #    {"Use-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"},
        #    {"Use-Agent": "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10"},
        #    {"Use-Agent": "Opera/8.0 (Windows NT 5.1; U; en)"},
        #    {"Use-Agent": "Openwave/ UCWEB7.0.2.37/28/999"},
        #    {"Use-Agent": "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"},
        #    {"Use-Agent": "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"},
        #    {"Use-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16"},
        #]
        self.count = 0
        self.proxy_url = 'http://www.xicidaili.com/nt/'
        self.proxy_ip = []
        self.proxy_ip_usable = []


    def get_proxy_ip(self):
        # headers = {'Use-Agent': "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"}
        for i in range(1, 2):
            req = Request(self.proxy_url + str(i))
            req.add_header("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)"
                                     " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.")
            html = urlopen(req).read()
            time.sleep(10)
            html_txt = decode_html(html)
            bs_obj = BeautifulSoup(html_txt, 'html.parser')
            # print(html_txt)
            ip_list_nodes = bs_obj.find_all('tr', class_='odd')
            # print(ip_list_nodes)
            for ip in ip_list_nodes:
                ip_address = ip.td.next_sibling.next_sibling
                ip_port = ip_address.next_sibling.next_sibling
                #print(ip_address)
                # print(ip_port)
                # print(ip_address.get_text())
                self.proxy_ip.append(ip_address.get_text() + ':' + ip_port.get_text())
                # print(self.proxy_ip)


        return self.proxy_ip

    def update_ip_proxy(self):
        self.proxy_ip_usable = self.get_proxy_ip()
        print(self.proxy_ip_usable)
        # print(self.proxy_ip_usable)


    def get_html_txt_(self, page_url):
        # ip_proxy = '180.168.179.193:8080'
        # ip_proxy = self.proxy_ip[0]
        for k in range(100):
            try:
                if self.proxy_ip_usable == []:
                    self.update_ip_proxy()
                proxy = {'http': str(self.proxy_ip_usable.pop())}
                print(proxy)
                proxy_support = ProxyHandler(proxy)
                opener = build_opener(proxy_support)
                install_opener(opener)
                response = urlopen(page_url, timeout=5)
                html = response.read()
                print(response.getcode())
                html_txt = decode_html(html)
                return html_txt

            except:
                pass
        return None

    def get_html_txt(self, page_url):
        html = urlopen(page_url).read()
        html_txt = decode_html(html)
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
                else:
                    self.new_position_list_urls.append(url)
                    url_file = open('url_file.txt', 'a')
                    url_file.write(url + '\n')
                    url_file.close()
        except:
            print('+++++++++++++++++访问和解析页面失败了++++++++++++++++++++')
        return self.new_position_list_urls

    def get_data_from_list_page(self, list_page):
        # 传入一个职位列表Url，然后从此解析职位页面Url，然后抽取信息
        # list_page = 'http://s.138job.com/hire/1?keyword=&workadd=0&keywordtype=1&position=2212'
        html_txt = self.get_html_txt(list_page)
        bs_obj = self.get_bs_obj(html_txt)
        position_info_pages = []
        if bs_obj == None:
            print("-----------解析职位列表信息页面失败------------")
            return
        else:
            positon_list = bs_obj.find_all('a', href=re.compile('.*H.*'))
            for i in positon_list:
                position_info_pages.append(i['href'])
            # print(position_info_pages)
            for page in position_info_pages:
                print(page)
                html_txt1 = self.get_html_txt(page)
                bs_obj1 = self.get_bs_obj(html_txt1)
                # print(bs_obj1)
                if bs_obj1 == None:
                    print('===============解析职位具体信息页面失败============')
                else:
                    self.get_and_write_data_from_position_page(bs_obj1)

    def get_and_write_data_from_position_page(self,bs_obj):
        job_name = job_name_from_bs(bs_obj)
        store_name = store_name_from_bs(bs_obj)
        # address_from_bs(bs_obj)
        # store_name
        info_file = open('info.txt', 'a')
        info_file.write(job_name+'~'+store_name+'\r\n')
        info_file.close()

    def main(self, i):
        self.get_position_page(i)
        for num in range(len(self.new_position_list_urls)):
            list_page = self.new_position_list_urls.pop()
            self.old_position_list_urls.append(list_page)
            self.get_data_from_list_page(list_page)

if __name__ == '__main__':
    obj = RequestRenCai()
    # pool = Pool(processes=20)
    for i in range(1000, 2500):
        try:
            print(i)
            obj.main(i)
            # pool.apply_async(obj.main, (i,))
            # obj.get_proxy_ip()

        except:
            pass