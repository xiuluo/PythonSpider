#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from ProxyCrawl import *
import requests
import time

uid = '2039695'  # 用户ID，在签到页面可以看见
pid = 1023  # 每日主题的id，不是必须的，据我观察是每天递增的
pid += (datetime.datetime.now() - datetime.datetime(2017, 10, 20)).days
shared_url = 'http://www.maimemo.com/share/page/?uid=' + uid + '&pid=' + str(pid)

if __name__ == '__main__':
    proxy_list = get_proxy_ip()
    for proxy_ip in proxy_list:
        proxy_ip = {'http': 'http://' + proxy_ip}
        try:
            request = requests.get(shared_url, proxies=proxy_ip, timeout=0.1)
        except:
            continue
        if request.status_code == 200:
            print("通过", proxy_ip, "成功点击链接\n")
            time.sleep(1)
        else:
            print("代理连接失败\n")