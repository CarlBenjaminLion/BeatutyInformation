# coding=utf-8
from urllib.request import *
from bs4 import BeautifulSoup
import chardet
import re
from multiprocessing import Pool

rencai_url = 'http://s.138job.com/hire/'
canshu = '?workadd=0&keywordtype=1&position='


def get_bs_obj(page_url):
    try:
        # print('begin')
        html = urlopen(page_url).read()
        # print(html)
        html_txt = decode_html(html)
        # print(html_txt)
        bs_obj = BeautifulSoup(html_txt, 'html.parser')
    except:
        return None
    return bs_obj


def decode_html(html):
    pass
    html_text = html.decode(chardet.detect(html)['encoding'], 'ignore')
    return html_text


def get_position_page(i):
    url_list = []
    try:
        for j in range(1, 100):
            url = rencai_url + str(j) + canshu + str(i)
            print(url)
            bs_obj = get_bs_obj(url)  # --function--
            weiye = bs_obj.find_all('div', class_='pager')
            if weiye == []:
                return
            else:
                url_list.append(url)
                # print('add sucess')
                url_file = open('url_file.txt', 'a')
                url_file.write(url + '\n')
                url_file.close()

    except:
        print('+++++++++++++++++访问和解析页面失败了++++++++++++++++++++')

    return url_list


def judge_not_none_and_return_url():
    # url_data = {}
    for i in range(1000, 3000):
        try:
            print(i)
            list = get_position_page(i)


        except:
            pass


def get_data_from_list_page(list_page):
    bs_obj = get_bs_obj(list_page)
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
        bs_obj1 = get_bs_obj(page)
        if bs_obj1 == None:
            print('===============解析职位具体信息页面失败============')
        else:
            info_collect(bs_obj1)


# ==============================================Information Collection===================================================

def info_collect(bs_obj):
    '''
    job_name
    store_name
    provice_name
    address
    person_name
    phone_name
    introduction

    :param bs_obj:
    :return: info_result_in_dict
    '''
    '''div_job_name_node = bs_obj.find('div', class_='jobs_name')
    if div_job_name_node == None:
        div_job_name_node = bs_obj.find('h1', class_='job_item_title')
        job_name = div_job_name_node.get_text()
    else:
        job_name = div_job_name_node.get_text()
    print(job_name)'''


def job_name_from_bs(bs_obj):
    div_job_name_node = bs_obj.find('div', class_='jobs_name')
    if div_job_name_node == None:
        div_job_name_node = bs_obj.find('h1', class_='job_item_title')
        job_name = div_job_name_node.get_text()
    else:
        job_name = div_job_name_node.get_text()
    print(job_name)
    pass


def store_name_from_bs(bs_obj):
    pass


def provice_name_from_bs(bs_obj):
    pass


def address_from_bs(bs_obj):
    pass


def person_name_from_bs(bs_obj):
    pass


def phone_number_from_bs(bs_obj):
    pass


def inrotduction_from_bs(bs_obj):
    pass


# ==============================================Information Collection===================================================

def main():
    judge_not_none_and_return_url()
    # get_data_from_list_page('http://s.138job.com/hire/11?workadd=0&keywordtype=1&position=1000')
    pass


main()
