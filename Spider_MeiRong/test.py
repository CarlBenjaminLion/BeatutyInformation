# coding=utf-8
from selenium import webdriver
import requests
from urllib.request import *
from bs4 import BeautifulSoup
import time


class UrlOpen(object):

    def __init__(self):
        self.root_url = 'http://www.138job.com/'
        self.test_url_1 = 'http://www.138job.com/shtml/Company/18401/H_472787.shtml'
        self.load_contact = 'http://www.138job.com/AjaxMethods/AjaxLoadContacts.aspx'
        self.proxy_url = 'http://www.xicidaili.com/nt/'
        self.proxy_ip = []


    def get_page(self):
        url = self.test_url_1
        driver = webdriver.PhantomJS(executable_path='./JS/bin/phantomjs')
        driver.get(url)
        print(driver.page_source)

    def get_contact_info(self, refer):
        headers = {

            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': "*/*",
            'Accept-Language': "zh,en-US;q=0.7,en;q=0.3",
            'Accept-Encoding': "gzip, deflate",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'X-Requested-With': "XMLHttpRequest",
            'Referer': refer,
            'Content-Length':'78',
            'Cookie': 'Hm_lvt_23f92bee2e6092174ba68c613da8fa2e=1504598938,1504603469,1504621364,1504621366; search_hire_history=%5B%7B%22title%22%3A%22%E7%BA%B9%E7%BB%A3%E7%BE%8E%E7%94%B2%E7%B1%BB%22%2C%22url%22%3A%22keyword%3D%26workadd%3D0%26keywordtype%3D1%26position%3D1000%22%7D%2C%7B%22title%22%3A%22%E7%BE%8E%E5%AE%B9%E9%99%A2%E5%BA%97%E9%95%BF%22%2C%22url%22%3A%22keyword%3D%26workadd%3D0%26keywordtype%3D1%26position%3D2212%22%7D%5D; bdshare_firstime=1504502712827; AJSTAT_ok_times=1; pgv_pvi=3216969728; safedog-flow-item=67365999200E71B7ADDDC24062A1A914; search_city_id=1012; search_city_name=%E5%90%89%E6%9E%97; Hm_lpvt_23f92bee2e6092174ba68c613da8fa2e=1504624841',
            'Connection': "keep-alive",
        }
        data = {
            'action': 'hirecontacts',
            #'hideEmailTxt': '1',
            'comId': '1280608',
            'hireId': '472787',
        }
        r = requests.post(self.load_contact,data=data)
        print(r.status_code)
        print(r.text)
        print(r.encoding)

    def get_proxy_ip(self):
        for i in range(1, 2):
            print(i)
            headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)"
                                     " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57."}
            html_txt = requests.get(self.proxy_url + str(i), headers=headers).text
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
            print(self.proxy_ip)


if __name__ == '__main__':
    test_obj = UrlOpen()
    # test_obj.get_page()
    test_obj.get_contact_info(test_obj.test_url_1)
    # test_obj.get_proxy_ip()
