# -*- coding: utf-8 -*
import random
import requests
import time
import datetime


def send_post(url, header, timestamp, *json):
    global r  # 只保存最后一个请求的响应结果
    for data in json:
        ms = int(round(time.time() * 1000))
        # 有些post的包需要发送两个时间戳，作用未知
        if timestamp == 1:
            url += '?v=' + ms.__str__()
        elif timestamp == 2:
            url += '?v=' + ms.__str__() + '&_=' + (ms + 5).__str__()
        r = requests.post(url, json=data, headers=header)
    return r


desk_list = [62, 63, 64, 65, 66, 54, 53, 52, 51, 50, 15, 16, 17, 18, 19, 20, 21, 9, 8, 7, 6, 5, 4]  # 位置不错的桌子
seat_list = ['A', 'B', 'E', 'F']  # 不喜欢坐中间

service_url = 'http://211.70.171.14:9999/tsgintf/main/service'
headers = {'Accept': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; ZUK Z2121 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 Html5Plus/1.0',
           'Origin': 'file://',
           'X-Requested-With': 'XMLHttpRequest',
           'Content-Type': 'application/json',
           'Cookie': 'JSESSIONID=2597797C789E48741A70308E38D87F31'
           }

UPD_VERSION_data = {"intf_code": "UPD_VERSION", "params": {"platform": "0"}}  # 查询更新
LOGIN_data = {"intf_code": "QRY_LOGIN", "params": {"userPhysicalCard": "2014014053", "password": "保密"}}  # 模拟登陆
QRY_ADVERT_data = {"intf_code": "QRY_ADVERT", "params": {}}  # 未知。。。
QRY_NOTICE_data = {"intf_code": "QRY_NOTICE", "params": {"limit": "5"}}  # 系统通知
QRY_MY_PRE_SEAT_CHECK_data = {"intf_code": "QRY_PRE_SEAT_CHECK", "params": {"userPhysicalCard": "2014014053"}}  # 预约记录查询
QRY_PRE_LIBRARY_data = {"intf_code": "QRY_PRE_LIBRARY",
                        "params": {"userPhysicalCard": "2014014053"}}  # 查看图书馆(然而渣校就一个图书馆）
QRY_OPENHOURS_data = {"intf_code": "QRY_OPENHOURS", "params": {"libraryId": "1"}}  # 选择图书馆
QRY_PRE_SEAT_CHECK_data = {"intf_code": "QRY_PRE_SEAT_CHECK",
                           "params": {"userPhysicalCard": "2014014053", "dateStr": "2017-5-13", "startHour": "06:00",
                                      "endHour": "11:00"}}  # 指定时段座位信息查询
QRY_PRE_ROOM_data = {"intf_code": "QRY_PRE_ROOM",
                     "params": {"dateStr": "2017-5-11", "libraryId": "1", "startHour": "6:00",
                                "endHour": "23:00"}}  # 查询指定自习室
QRY_PRE_SEAT_data = {"intf_code": "QRY_PRE_SEAT",
                     "params": {"roomId": "10", "dateStr": "2017-5-11", "startHour": "6:00",
                                "endHour": "23:00"}}  # 查询座位
UPD_PRE_SEAT_data = {"intf_code": "UPD_PRE_SEAT",
                     "params": {"seatNo": "43B", "roomId": "10", "dateStr": "2017-5-11", "startHour": "6:00",
                                "endHour": "23:00", "userPhysicalCard": "2014014053"}}  # 抢座！

now_day = datetime.datetime.now().strftime('%Y-%m-%d')
start_hour = datetime.datetime.now().hour + 1

QRY_PRE_SEAT_CHECK_data['params']['dateStr'] = now_day
QRY_PRE_ROOM_data['params']['dateStr'] = now_day
QRY_PRE_SEAT_data['params']['dateStr'] = now_day
UPD_PRE_SEAT_data['params']['dateStr'] = now_day
UPD_PRE_SEAT_data['params']['startHour'] = start_hour.__str__() + ':00'
start_hour += 5  # 一次只能预定五个小时的座位
UPD_PRE_SEAT_data['params']['endHour'] = start_hour.__str__() + ':00'

# 开始模拟预约座位
r = send_post(service_url, headers, 0, UPD_VERSION_data, LOGIN_data)  # 客户端每次打开都要检查更新
headers['Cookie'] = 'JSESSIONID=' + r.cookies['JSESSIONID']
headers['X-Requested-With'] = 'io.dcloud.H507AAC9B'
headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
send_post(service_url, headers, 1, QRY_ADVERT_data, QRY_NOTICE_data, QRY_MY_PRE_SEAT_CHECK_data)  # 参考客户端发包顺序，没有实际意义
send_post(service_url, headers, 2, QRY_PRE_LIBRARY_data, QRY_OPENHOURS_data,
          QRY_PRE_SEAT_CHECK_data)  # 查询图书馆各个自习室的空间情况
send_post(service_url, headers, 1, QRY_PRE_ROOM_data, QRY_PRE_SEAT_data)  # 查询选定的自习室(203)以及座位的空闲情况

cnt = 0
while True:
    cnt += 1
    random_seat = str(desk_list[random.randint(0, len(desk_list) - 1)]) + seat_list[
        random.randint(0, len(seat_list) - 1)]  # 每次座位都一样未免有些太招摇了
    UPD_PRE_SEAT_data['params']['seatNo'] = random_seat
    r = send_post(service_url, headers, 1, UPD_PRE_SEAT_data)
    rs = r.json()
    if rs['result_code'] == '0' or cnt >= 30:
        print r.text
        break
