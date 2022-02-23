#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   Cub0ne
#   E-mail  :   mkyrie05@gmail.com
#   Date    :   2022-02-21 15:36
#   Desc    :   获取相关域名对应的最新 IP

import datetime
import requests
from bs4 import BeautifulSoup


def _request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.212 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


address_ip = {}


def _parse(html_data, site):
    if html_data is None:
        return
    soup = BeautifulSoup(html_data, 'lxml')
    try:
        address = soup.find(id='dnsinfo').find_all('tr')
        for tr in address:
            if tr.find_all('td')[1].text == 'A':
                ip = tr.find('a').text
                if ip is not None:
                    address_ip[site] = ip
                    print(ip + "\t" + site)
                    break
    except AttributeError as error:
        print(error)


def _update():
    print(address_ip)
    today = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    f = open("hosts.txt", "w")
    f.write("# Update Host Start\n")
    for key in address_ip:
        f.write(address_ip[key] + "\t" + key + "\n")
    f.write("# Update Host End " + today + " 更新\n")
    f.close()


if __name__ == '__main__':
    domains = []
    ipaddress = 'https://ipaddress.com/website/'
    with open('domain.txt', 'r', encoding='utf-8') as d:
        for line in d.readlines():
            domains.append(line.strip())
        print(domains)

    for domain in domains:
        html = _request(ipaddress + domain)
        _parse(html, domain)

    _update()
