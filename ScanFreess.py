#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import base64
import requests
import json

configPath = "D:\Soft\Shadowsocks\gui-config.json"


def deCode():
    count = 0
    while True:
        r = requests.post('http://cli.im/Api/Browser/deqr', data={'data': 'http://freess.org/images/servers/jp01.png'})
        res = r.json()
        if res["status"] == 1 and count < 10:  # 最多请求十次
            return res
            break
        count += 1


def fetchSSInfo():
    res = deCode()
    rawData = res['data']['RawData'][5:]
    ss = base64.b64decode(rawData).decode()
    subss = str(ss).split(':')
    mod = subss[0]
    pwd = str(ss).split(':')[1].split('@')[0]
    ip = str(ss).split(':')[1].split('@')[1]
    port = subss[2].strip()
    list = [ip, port, pwd, mod]
    return list


def modifyConfigJson():
    ssInfo = fetchSSInfo()
    # 读取配置文件
    with open(configPath, 'r') as f:
        ssConfig = json.load(f)
    ssConfigList = ssConfig["configs"]
    for data in ssConfigList:
        if data['remarks'] == "freess":
            data['server'] = ssInfo[0]
            data['server_port'] = ssInfo[1]
            data['password'] = ssInfo[2]
            data['method'] = ssInfo[3]
            break
    with open(configPath, 'w') as f:
        json.dump(ssConfig, f, indent=2)


modifyConfigJson()
