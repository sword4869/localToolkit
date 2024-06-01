import configparser
import datetime
import threading
from time import *
import random
import requests
import urllib3

# for InsecureRequestWarning
urllib3.disable_warnings()

url_init = 'https://druidv6.if.qidian.com/argus/api/v1/common/comment/publish'

headers = {
}


def func():
    config = configparser.ConfigParser(interpolation=None)
    config.read("demo2.ini")

    section_list = config.sections()
    for section in section_list:
        with open(r'log.txt', 'a', encoding='utf-8') as fp:
            headers_each = headers

            # headers_each[''] = config[section]['']
            headers_each['Cookie'] = config[section]["Cookie"]
            headers_each['abtest-gzip'] = config[section]["abtest-gzip"]
            headers_each['QDInfo'] = config[section]["QDInfo"]
            headers_each['User-Agent'] = config[section]["User-Agent"]
            headers_each['gorgon'] = config[section]["gorgon"]
            headers_each['AegisSign'] = config[section]["AegisSign"]
            headers_each['borgus'] = config[section]["borgus"]
            headers_each['QDSign'] = config[section]["QDSign"]
            headers_each['Content-Type'] = config[section]['Content-Type']
            headers_each['Content-Length'] = config[section]['Content-Length']
            headers_each['Host'] = config[section]['Host']
            headers_each['Connection'] = config[section]['Connection']
            headers_each['Accept-Encoding'] = config[section]['Accept-Encoding']

            # dynamic
            headers_each['tstamp'] = '{:.3f}'.format(time()).replace('.','')
            
            # for k,v in enumerate(headers_each):
            #     print(k, v, type(headers_each[v]), headers_each[v])

            body = config[section]["body"]

            response = requests.post(
                url=url_init, data=body, headers=headers_each, verify=False)
            print('[{}] [{}]'.format(
                section, strftime("%Y-%m-%d %H:%M:%S", localtime())))
            item2 = [
                '[{}] [{}]:'.format(
                    section, strftime("%Y-%m-%d %H:%M:%S", localtime())),
                response.text, '\n'
            ]
            fp.writelines(item2)
            fp.write('\n')
        sleep(random.randint(1, 10))

    # 如果需要循环调用（父生子，子生孙），就要添加以下方法
    # timer = threading.Timer(86400, func)
    # timer.start()


def timer():
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
    func()
