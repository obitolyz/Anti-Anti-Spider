#!/usr/bin/env python
# encoding: utf-8

# @author: obitolyz
# @file: ip_proxy.py
# @time: 2018/5/6 21:16

# description: ip代理池
# original: http://www.xicidaili.com/wt/

import requests
import random
from bs4 import BeautifulSoup as bs

sess = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


# 从西刺代理那里获取ip和端口
def gain_ip_port():
    response = sess.get('http://www.xicidaili.com/wt/', headers=headers)
    response.encoding = response.apparent_encoding
    # print(response.text)
    soup = bs(response.text, 'html.parser')
    table = soup.find('table', {'id': 'ip_list'})
    trs = table.find_all('tr')[1:]
    ip_list = []
    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[1].string
        port = tds[2].string
        ip_list.append(ip+':'+port)
    return ip_list


# 访问百度来测试ip是否可用
def checkout_valid(ip):
    try:
        html = sess.get('http://www.baidu.com', proxies={'http': ip}, headers=headers)
        return html.status_code == 200
    except Exception as e:
        return False


def main():
    ip_pool = gain_ip_port()
    url = 'http://www.whatismyip.com.tw/'  # 用于测试ip
    proxies = {
        'http': ''
    }
    ip = random.choice(ip_pool)
    while not checkout_valid(ip):
        ip_pool.remove(ip)
        ip = random.choice(ip_pool)

    proxies['http'] = ip
    response = sess.get(
        url,
        proxies=proxies,
        headers=headers
    )
    response.encoding = response.apparent_encoding
    print(response.text)

if __name__ == '__main__':
    main()
