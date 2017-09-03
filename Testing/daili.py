"""
此处为代理IP的爬取（更换）
1.爬取代理IP，我将对西刺网下手
2.测试代理IP是否合格（测试对象http://www.baidu.com)
3.将合格的代理IP存储在数据库中
运行环境是Win
"""

import requests
from bs4 import BeautifulSoup
import lxml
import time
import random
class Daili(object):
    def __init__(self):
        self.temp = []
        self.num=0
        self.get_ip()
        self.test()
    def get_ip(self):
    #get ip and
        for n in range(1000):
            time.sleep(random.randint(3,9))
            url = "http://www.xicidaili.com/nn/"+str(n)
            headers = {"Use-Agent":"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"}
            get_data = requests.get(url,headers=headers)

            bsobj = BeautifulSoup(get_data, "lxml")
            table = bsobj.find("table", id="ip_list").find_all("tr")
            for row in table:
                data = row.find_all(text=True)
                if not data[1] == "国家":
                    # print(data)
                    self.temp.append(data[2] + ":" + data[4])
                    self.num+=1
            #print(self.temp)
            print(self.num)
            with open(r"F:/11.txt", "a") as fd:
                for num in self.temp:
                    fd.write(num + "\n")
            print("over")
    def test(self):
        #test
        for r in open(r"F:/11.txt","r"):
            proxy = str(r)
            test = requests.get("http://www.baidu.com",proxies=proxy)
            if test.status_code == 200:
                print(r)#to store the daili
                with open(r"F:/12.txt","a") as fd:
                    fd.write(r + "\n")
            else:
                pass


if __name__ == '__main__':
    obj = Daili()
    obj.get_ip()
    obj.test()

