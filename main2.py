import json
import os
import requests
from threading import Timer
import datetime
import schedule
import time


def get_token():
    global access_token
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
    r1 = requests.get(url, headers=headers, params=params1)
    access_token = eval(r1.content.decode())['access_token']
    print("access_token:",access_token)
    Timer(3600, get_token).start()

def remind():
    with open("new_people_userid.txt", "r") as f:
        new_people_list = f.readlines()

    if len(new_people_list) != 0:
        for i in range(len(new_people_list)):
            url5 = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
            params5 = {'access_token': access_token}
            now = datetime.datetime.now()
            ta = now.strftime('%Y-%m-%d %H:%M:%S')
            body = {
                "touser": new_people_list[i].split('\n')[0],
                "msgtype": "textcard",
                "agentid": "1000004",
                "textcard": {
                    "title": "小提醒~~",
                    "description": "<div class=\"gray\">" + ta + "</div> <div class=\"normal\">请尽快向人事提交资料，如已经提交，忽略此消息即可~</div><div class=\"highlight\"></div>",
                    "url": "null"
                },
                "enable_id_trans": 0,
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800
            }
            try:
                r5 = requests.post(url5, params=params5, data=json.dumps(body))
                print(r5.status_code)
                print("向" + new_people_list[i] + "发送提醒成功！")
            except requests.exceptions.RequestException as e:
                print("向" + new_people_list[i] + "发送提醒失败！")
                continue
        os.remove('/home/qiwei_yingxin/new_people_userid.txt')


schedule.every().day.at("17:30").do(remind)
get_token()
while True:
    schedule.run_pending()
    time.sleep(1)
