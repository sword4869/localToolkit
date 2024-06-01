import configparser
import datetime
import sys
import threading
from time import *
import random
import requests
import urllib3

# for InsecureRequestWarning
urllib3.disable_warnings()

url_wujian = 'https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save'

headers = {
    'https': '//xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save HTTP/1.1',
    'Host': 'xxcapp.xidian.edu.cn',
    'Connection': 'keep-alive',
    'Content-Length': '2073',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://xxcapp.xidian.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; vivo X9 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2581 MMWEBSDK/200601 Mobile Safari/537.36 MMWEBID/77 MicroMessenger/7.0.16.1700(0x27001035) Process/toolsmp WeChat/arm64 NetType/WIFI Language/zh_CN ABI/arm64',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://xxcapp.xidian.edu.cn/site/ncov/xidiandailyup',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}


def func():
    config = configparser.ConfigParser(interpolation=None)
    config.read("demo1.ini")

    section_list = config.sections()
    for section in section_list:
        with open(r'log.txt', 'a', encoding='utf-8') as fp:
            headers_each = headers
            headers_each['Cookie'] = config[section]["Cookie"]
            name = config[section]["name"]
            body = config[section]["xd"]
            response = requests.post(
                url=url_wujian, data=body, headers=headers_each, verify=False)
            print('[{}][{}][{}]'.format(
                section, name, strftime("%Y-%m-%d %H:%M:%S", localtime())))
            item2 = [
                '[{}][{}][{}]:'.format(
                    section, name, strftime("%Y-%m-%d %H:%M:%S", localtime())),
                response.text, '\n'
            ]
            fp.writelines(item2)
            fp.write('\n')
        sleep(random.randint(1, 10))

    # 如果需要循环调用（父生子，子生孙），就要添加以下方法
    # timer = threading.Timer(86400, func)
    # timer.start()


# 获取现在时间
now_time = datetime.datetime.now()
now_year = now_time.date().year
now_month = now_time.date().month
now_day = now_time.date().day

# 获取明天时间
# next_time = now_time + datetime.timedelta(days=+1)

time_list = ["08:05:01", "13:05:01", "18:05:01"]
timer_start_time_list = []

for _ in time_list:

    next_time1 = datetime.datetime.strptime(
        str(now_year) + "-" + str(now_month) + "-" + str(now_day) + " " + _, "%Y-%m-%d %H:%M:%S")

    # 秒
    timer_start_time = (next_time1 - now_time).total_seconds()
    if(timer_start_time < -60*60*5):
        continue

    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time, func)
    timer.start()
