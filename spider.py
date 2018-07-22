# 爬取长春大学研究生导师姓名和照片


import re
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import os
from hashlib import md5

name = []


# 获取html
def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


# 解析导师总揽页面
def parse_page(html):
    print('解析开始......')
    soup = BeautifulSoup(html, 'lxml')
    for a in soup.select('a.aclass'):
        name.append(a.get_text())  # 添加导师的姓名
        print('获取到-%s-导师主页' % (a.get_text()))
        url_home = 'http://yjsb.ccu.edu.cn/' + a.attrs['href']  # 导师的个人简介页面url
        html_home = get_page(url_home)  # 获取导师个人简介页面html
        parse_home_page(html_home)  # 解析导师个人简介页面


# 解析导师个人简介页面
def parse_home_page(html_home):
    print('\t开始解析导师主页信息......')
    soup = BeautifulSoup(html_home, 'lxml')
    if soup.select('span img'):
        for img in soup.select('span img'):
            print('\t\t成功获取到导师照片链接，即将开始下载......')
            imag_url = 'http://yjsb.ccu.edu.cn/' + img.attrs['src']  # 导师照片链接
            download_image(imag_url)  # 下载照片
    if soup.select('p img'):
        for img in soup.select('p img'):
            print('\t\t成功获取到导师照片链接，即将开始下载......')
            imag_url = 'http://yjsb.ccu.edu.cn/' + img.attrs['src']  # 导师照片链接
            download_image(imag_url)  # 下载照片
    else:
        name.pop()
        print('\t\t获取导师照片链接失败，跳过。。。。。。。。。。。。。。。。。。。。。。。')


# 下载照片
def download_image(url):
    print('\t\t\t正在下载...')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_imag(response.content)
            print('\t\t\t\t下载成功!!!')
        else:
            return None
    except RequestException:
        return None


# 保存照片
def save_imag(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), name[-1], 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main():
    url = 'http://yjsb.ccu.edu.cn/dsdw.aspx'
    html = get_page(url)
    parse_page(html)


if __name__ == '__main__':
    main()
