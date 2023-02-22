import json
import time

import requests
import numpy as np
from threading import Timer
import datetime
from urllib3 import encode_multipart_formdata
from collections import OrderedDict


def get_token():
    global access_token, talk_access_token
    headers = {
        'pragma': "no-cache",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.8",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'cache-control': "no-cache",
        'connection': "keep-alive",
    }

    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    params1 = {'corpid': 'wwd447cfa59b842fbb', 'corpsecret': 'Mhnt4qntF9WbffhmgrhAcNNnw0EcdwsPqxxh1oeBlOE'}
    params2 = {'corpid': 'wwd447cfa59b842fbb', 'corpsecret': 'TW56hMYrS8-dzpiDh0tefX0s2WZYknuadGcx-oe3-Pc'}
    r1 = requests.get(url, headers=headers, params=params1)
    r2 = requests.get(url, headers=headers, params=params2)

    access_token = eval(r1.content.decode())['access_token']
    talk_access_token = eval(r2.content.decode())['access_token']
    print("access_token:", access_token)
    print("talk_access_token", talk_access_token)
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print("获取token的时间：", now)
    Timer(3600, get_token).start()


def get_media_id():
    global media_id
    headers = {
        "Content-Type": "multipart/form-data; boundary=---------------------------10159497931724953517101195095",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
    }

    url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload"
    params = {'access_token': access_token, 'type': 'file'}

    files = OrderedDict(
        [("file", ("mode.xlsx", open("/home/qiwei_yingxin/xxx.xlsx", 'rb').read(),  # 上传文件的路径
                   'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
         ("token", (None,
                    access_token,
                    "form-data")),
         ("fileType", (None, "file", "form-data")),
         ("uploadUrl", (None, "https://qyapi.weixin.qq.com/cgi-bin/media/upload", "form-data")),
         ])
    m = encode_multipart_formdata(files, boundary="---------------------------10159497931724953517101195095")
    res = requests.post(url, params=params, headers=headers, data=m[0])
    media_id = eval(res.text)['media_id']
    Timer(86400, get_token).start()


def jiance():
    # 获取所有员工的userid
    url3 = "https://qyapi.weixin.qq.com/cgi-bin/user/list_id"
    params3 = {'access_token': talk_access_token}
    body = {
        "cursor": "",
        "limit": 10000
    }
    r3 = requests.post(url3, params=params3, data=json.dumps(body))
    a = r3.content.decode()
    content = eval(r3.content.decode())  # str转为字典格式

    userid_list = []
    num = 0
    for i in content['dept_user']:
        # userid_list[num] = i['userid']
        userid_list.append(i['userid'])
        num += 1

    # 检测是否有新员工加入,检测到加入userid_list_all

    # new_people = ""
    for x in range(len(userid_list)):
        # 获取userid.txt内容
        userid_list_all = np.loadtxt('userid.txt', dtype=str, delimiter=' ')

        if userid_list[x] not in userid_list_all:
            print("欢迎" + userid_list[x] + "加入矢安科技！！！")

            file = open('new_people_userid.txt', mode='a', encoding='utf-8', newline="")
            file.write(userid_list[x])
            file.write("\n")
            file.close()

            file = open('userid.txt', mode='a', encoding='utf-8', newline="")
            file.write("\n")
            file.write(userid_list[x])
            file.close()

            url4 = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
            params4 = {'access_token': access_token}
            # body发送图文消息，body2发送文本消息，body3发送文件消息
            body = {
                "touser": userid_list[x],
                "msgtype": "news",
                "agentid": "1000004",
                "news": {
                    "articles": [
                        {
                            "title": "欢迎来到矢安科技！",
                            "description": "新员工入职指北，看完这篇，懂得都懂~",
                            "url": "https://open.work.weixin.qq.com/wwopen/mpnews?mixuin=KIJODAAABwDZtR1YAAAUAA&mfid=WW0321-aIpJCQAABwBY_Agds4n8fgJ8b7Z72&idx=0&sn=07018e74e294a94e2a9be0df97a4e54f&auth=1&state=",
                            "picurl": "https://wework.qpic.cn/wwpic/596715_85VnzHJqR3CDrsE_1676964715/0",

                        }
                    ]
                },
                "enable_id_trans": 0,
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800
            }

            body2 = {
                "touser": userid_list[x],
                "msgtype": "text",
                "agentid": "1000004",
                "text": {
                    "content": "请今天内将下面的员工履历表填好发给HR~"
                },
                "safe": 0,
                "enable_id_trans": 0,
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800
            }

            body3 = {
                "touser": userid_list[x],
                "msgtype": "file",
                "agentid": "1000004",
                "file": {
                    "media_id": media_id
                },
                "safe": 0,
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800
            }

            try:
                r4 = requests.post(url4, params=params4, data=json.dumps(body))
                time.sleep(5)
                r5 = requests.post(url4, params=params4, data=json.dumps(body2))
                time.sleep(1)
                r6 = requests.post(url4, params=params4, data=json.dumps(body3))
                print("向" + userid_list[x] + "发送消息成功！")
            except requests.exceptions.RequestException as e:
                print("发送消息失败")
                continue

    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    Timer(30, jiance).start()


get_token()  # 获取应用和通讯录的token
get_media_id()  # 将履历表.xlsx上传到临时资源获取media_id
jiance()  # 发送入职指北、提示、履历表
