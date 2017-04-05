#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import base64
import os
import requests
import json
from subprocess import call, Popen

configPath = "D:\Soft\Shadowsocks\gui-config.json"
ssClientPath = "D:\Soft\Shadowsocks\Shadowsocks.exe"


def deCode():
    count = 0
    # TODO 本地解析二维码
    # 在线解析二维码接口不稳定，粗暴的重复请求来解决
    while True:
        r = requests.post('https://cli.im/Api/Browser/deqr', data={'data': 'http://freess.org/images/servers/jp01.png'})
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
    # TODO 自动添加freess而不只是修改
    for data in ssConfigList:
        if data['remarks'] == "freess":
            data['server'] = ssInfo[0]
            data['server_port'] = ssInfo[1]
            data['password'] = ssInfo[2]
            data['method'] = ssInfo[3]
            break
    with open(configPath, 'w') as f:
        json.dump(ssConfig, f, indent=2)


def restartSSClient():
    os.system('taskkill /f /im Shadowsocks.exe')
    Popen(ssClientPath)


def main():
    modifyConfigJson()
    restartSSClient()


if __name__ == "__main__":
    main()
