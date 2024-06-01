import configparser
import datetime
import threading
from time import *
import requests
import urllib3
import json
import Notification
from fake_useragent import UserAgent


# for InsecureRequestWarning
urllib3.disable_warnings()

configFileName = "demo3.ini"
logFileName = 'log.txt'
# Running interval of program
# The post URL is not subject to DDoS restriction, so 10 seconds is allowed.
timeTick = 10

headers = {'User-Agent': UserAgent().random}


body = {}

dateNow = int(strftime("%d", localtime()))

# read ini configuration and fakerPost url


def func():
    sections = []

    config = configparser.ConfigParser(interpolation=None)
    config.read(configFileName, encoding='utf-8')

    section_list = config.sections()
    for index, section in enumerate(section_list):
        totalCount = None
        totalCountHistory = None
        NickName = None
        date = int(config[section]["date"])

        if date > dateNow:
            continue
        else:
            sections.append(section)

        circleId = config[section]["circleId"]
        postId = config[section]["postId"]
        totalCountHistory = config[section]["totalCountHistory"]
        NickName = config[section]["NickName"]
        url_base = config[section]["url_base"]
        url_complete = "{}circleId={}&postId={}".format(
            url_base, circleId, postId)
        # print(url_complete)
        response = requests.get(
            url=url_complete, data=body, headers=headers, verify=False)

        jsonData = json.loads(response.text)
        totalCount = jsonData['Data']['TotalCount']

        if int(totalCount) != int(totalCountHistory):
            message = '{}, {}!'.format(section, NickName)
            print(message)
            notification = Notification.Notification()
            notification.remote(title=message)
            notification.local()

    print('[{}] all pass.'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    with open(logFileName, 'a', encoding='utf-8') as fp:
        log_contents = [
            '------------------\n',
            '[{}]:{}\n'.format(
                strftime("%Y-%m-%d %H:%M:%S", localtime()), sections),
            '------------------\n'
        ]
        fp.writelines(log_contents)
    pass


def time_circle():

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


if __name__ == '__main__':
    try:
        while True:
            func()
            sleep(timeTick)
    except KeyboardInterrupt:
        message = 'ctrl-c to exit.'
        print(message)
    except:
        message = 'program error'
        print(message)
        notification = Notification.Notification()
        notification.remote(title=message)
    # time_circle()
