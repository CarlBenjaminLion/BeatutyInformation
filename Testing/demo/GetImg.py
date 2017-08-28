import re
import urllib.request


def getHtml(url=''):
    page = urllib.request.urlopen(url)
    html = page.read().decode('GBK')  # 解析网页源代码
    return html


# print(html)

def getImg(html):
    # https://cbu01.alicdn.com/img/ibank/2016/693/443/3382344396_1109687136.jpg
    # reg = r'https://.*\.?alicdn\.com[^"]+\.jpg'
    reg = r'//[\w]*\.?alicdn\.com[^"\']+\.jpg'  # 正则表达式，搜索匹配字段
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    print(len(imglist))
    x = 1
    for imgurl in imglist:
        print(imgurl)
        imgurl = 'https:' + imgurl
        urllib.request.urlretrieve(imgurl, 'save\\%s.jpg' % x)  # 按顺序保存在save文件夹
        x += 1


def DownLoadImg(url):
    html = getHtml(url)
    getImg(html)

