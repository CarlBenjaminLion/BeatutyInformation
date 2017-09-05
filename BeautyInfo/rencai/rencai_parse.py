# coding=utf-8
from urllib.request import *
from urllib.response import *
from bs4 import BeautifulSoup
import re


def job_name_from_bs(bs_obj):
    try:
        job_name_node = bs_obj.find('h1', class_='job_item_title')  # 华丽页面解析
        if job_name_node == None:
            job_name_node = bs_obj.find('div', class_='jobs_name')  # 朴实页面解析
            if job_name_node == None:
                job_name_node = bs_obj.find('div', class_='cfont')
                job_name = job_name_node.h1.get_text()
            else:
                job_name = job_name_node.b.get_text()


        else:
            job_name = job_name_node.get_text()
    except:
        print('解析职位名称失败')
        job_name = '无'
    print(job_name)
    return job_name

def store_name_from_bs(bs_obj):
    try:
        store_name_node = bs_obj.find('jobs_company_info')  # 华丽页面解析
        if store_name_node == None:
            store_name_node = bs_obj.find('title')  # 朴实页面解析
            store_name = store_name_node.get_text()
        else:
            store_name = store_name_node.dt.a.get_text()
    except:
        print('解析店铺名称失败')
        store_name = '无'
    print(store_name)
    return store_name

    pass


def address_from_bs(bs_obj):
    try:
        address_node = bs_obj.find('div', id='job_contact')
        print(address_node)
        if address_node == None:
            address_node = bs_obj.find('dl', id='newcontact')
            if address_node == None:
                print('ssss')
        print(address_node)
    except:
        pass
    pass


def person_name_from_bs(bs_obj):
    pass


def phone_number_from_bs(bs_obj):
    pass


def inrotduction_from_bs(bs_obj):
    pass


if __name__ == '__main__':
    pass