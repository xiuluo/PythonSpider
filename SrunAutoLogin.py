import json

import datetime
import requests
import time

def needLogin():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.62 Safari/537.36 '
    }
    url = "http://qq.com/"  # 判断能否联网的链接，因为深澜系统通过挟持HTTP插入js进行跳转的，所以需要判断一个状态码正常联网是302的链接
    res = requests.get(url, headers=headers,allow_redirects=False)
    if res.status_code == 200:
        return True
    else:
        return False


def doLogin(post, host):
    headers = {
        'Host': host,
        'Origin': 'http://' + host,
        'Referer': 'http://' + host + '/srun_portal_pc.php?url=&ac_id=1',
        'Content - Type': 'application / x - www - form - urlencoded',
        'Charset': 'UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.62 Safari/537.36 ',
    }
    auth_url = "http://" + host + "/include/auth_action.php"
    r = requests.post(auth_url, data=post, headers=headers)


def doLogout(post, host):
    headers = {
        'Host': host,
        'Origin': 'http://' + host,
        'Referer': 'http://' + host + '/srun_portal_pc_succeed.php',
        'Content - Type': 'application / x - www - form - urlencoded',
        'Charset': 'UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.62 Safari/537.36 ',
    }
    auth_url = 'http://' + host + '/srun_portal_pc_succeed.php'
    r = requests.post(auth_url, data=post, headers=headers)


if __name__ == '__main__':
    authIP = "211.70.160.3"  # 认证服务器的ip
    with open("netaccount.json", 'r') as load_f:
        load_dict = json.load(load_f)

    # 分时段使用不同的账号
    nowHour = datetime.datetime.now().hour
    if nowHour >= 23 or nowHour <= 7:
        index = 1
    else:
        index = 0
    account = load_dict['account'][index]['account']
    password = load_dict['account'][index]['password']
    loginPost = {
        'action': 'login', 'username': account, 'password': password, 'ac_id': 1, 'user_ip': '', 'nas_ip': '',
        'user_mac': '', 'save_me': 0, 'ajax': 1
    }
    logoutPost = {
        'action': 'auto_logout', 'info': ' ', 'user_ip': '211.70.170.71'
    }

    if nowHour == 23 or nowHour == 7:
        doLogout(logoutPost, authIP)
        time.sleep(3)
    if needLogin():
        doLogin(loginPost, authIP)
