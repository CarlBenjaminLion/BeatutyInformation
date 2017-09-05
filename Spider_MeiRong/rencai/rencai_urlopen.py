# coding=utf-8
import requests
from urllib.request import *
from bs4 import BeautifulSoup
import chardet
import time
import csv

url1 = 'http://www.138job.com/shtml/Company/18612/H_477200.shtml'  # 比较华丽的
url2 = 'http://www.138job.com/shtml/Company/18610/H_451248.shtml'  # 比较朴实的


def decode_html(html):
    pass
    html_text = html.decode(chardet.detect(html)['encoding'], 'ignore')
    return html_text


class RenCaiGetData(object):

    def __init__(self, url):
        self.domain_url = 'http://www.138job.com/'
        self.company_url = 'http://www.138job.com/shtml/Company/18612/'
        self.load_contact = 'http://www.138job.com/AjaxMethods/AjaxLoadContacts.aspx'
        self.url = url
        # self.data_of_contact = data_of_contact
        self.comId = '---'
        self.hireId = '---'
        self.job_name = '---'
        self.store_anme = '---'
        self.person = '---'
        self.address = '---'
        self.phone_img_url = '---'
        self.introduction = '---'

    def parse_hire_id(self):
        a = self.url.find('H_')
        # print(a)
        b = self.url.find('.shtml')
        # print(b)
        self.hireId = self.url[a + 2: b]
        return self.hireId

    def parse_com_id(self, bs_obj):
        try:

            node = bs_obj.find('dl', class_='jobs_company_info')  # 朴实
            if node == None:
                node = bs_obj.find('ul', class_='mainnav')  # 华丽
                text = node.li.a['href']
                a = text.find('C_')
                a +=2
                b =  text.find('.shtml')
                self.comId = text[a:b]
                store_name = bs_obj.find('div', class_='block_tips').get_text()
                c = store_name.find('信息由')
                d = store_name.find('发布')
                store_name = store_name[c+3:d]
                self.store_name = store_name
                introduction_node = bs_obj.find('div', class_='job_item_content')
                # print(introduction_node)
                introduction = introduction_node.get_text()
                self.introduction = introduction.replace(' ', '').replace('\n', '')



            else:
                text = node.dt.a['href']
                store_name = node.dt.a.get_text()
                a = text.find('C_')
                a += 2
                b = text.find('.shtml')
                self.comId = text[a:b]
                self.store_name = store_name
                introduction_node = bs_obj.find('div', class_='jobs_info')
                introduction = introduction_node.get_text()
                self.introduction =introduction.replace(' ', '').replace('\n', '')
        except:
            return None

    def set_type(self):
        pass

    def job_name_from_bs(self, bs_obj):
        try:
            job_name_node = bs_obj.find('h1', class_='job_item_title')  # 华丽页面解析
            if job_name_node == None:
                job_name_node = bs_obj.find('div', class_='jobs_name')  # 朴实页面解析
                job_name = job_name_node.b.get_text()


            else:
                job_name = job_name_node.get_text()
        except:
            print('解析职位名称失败 ' + self.url)
            job_name = '无'
        return job_name


    def address_and_person_from_bs(self):
        data ={
            'action': 'hirecontacts',
            'comId': self.comId,
            'hireId': self.hireId,
        }
        try:
            r = requests.post(self.load_contact, data=data)
            html = r.text
            time.sleep(0.5)
            bs_obj = BeautifulSoup(html, 'html.parser')
            phone_img_node = bs_obj.find('span', id='tel_2').img
            self.phone_img_url = phone_img_node['src']
            # print(self.phone_img_url)
            nodes = bs_obj.find_all('td')
            # print(nodes)
            address = nodes[-1].get_text()
            person  = nodes[-3].get_text()[0:3]
            self.address = address
            self.person = person
        except:
            pass

    def introduction_from_bs(self):
        pass




    def open(self):
        try:
            r = urlopen(self.url, timeout=5).read()
            html = decode_html(r)
            bs_obj = BeautifulSoup(html, 'html.parser')
        except:
            return None
        try:
            self.job_name = self.job_name_from_bs(bs_obj)
            if self.job_name == '无' or self.job_name == '' or self.job_name == None:
                print('无--')
                file = open('failed_urls.txt', 'a')
                file.write(self.url)
                file.close()
                return
            self.parse_com_id(bs_obj)
            self.parse_hire_id()
            self.address_and_person_from_bs()
            if self.person == '---' or self.person == ' [ ' or self.person == 'htt':
                file = open('failed_urls.txt', 'a')
                file.write(self.url)
                file.close()
                return
            if self.store_name == '---':
                file = open('failed_urls.txt', 'a')
                file.write(self.url)
                file.close()
                return
            file = open('info1.csv', 'a')
            writer = csv.writer(file)
            data = [self.job_name, self.store_name, self.person, self.address, self.phone_img_url, self.introduction, self.comId, self.hireId]
            writer.writerow(data)
            file.close()
        except:
            file = open('failed_urls.txt', 'a')
            file.write(self.url)
            file.close()


if __name__ == '__main__':
    obj = RenCaiGetData(url2)
    obj.open()
