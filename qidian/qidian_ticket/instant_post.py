###
# 即时版本。borgus过期就等邮件
###
import time
from urllib import response
import requests

from src.Poster import Poster
from src.Notification import Notification
from src.MyEmail import MyEmail
from src.TimeTransformer import TimeTransformer
from src.GetHeaders import GetHeaders

class MainPro:
    def __init__(self) -> None:
        self.poster = Poster()
        self.getHeaders = GetHeaders()
        
    def reload(self, type):
        try:
            headers = self.getHeaders.load(type)
            self.poster.reload_headers(headers, type)
        except FileNotFoundError:
            self.wait_email(type)

    def logger(self, headers):
        
        header_str_time = TimeTransformer().timestamp2str_time(int(headers['tstamp'])/1000)

        with open('log/log.txt', 'a', encoding='utf-8') as f:
            line = f"{headers['borgus']},{headers['tstamp']},{header_str_time}\n"
            f.write(line)

    def wait_email(self, type):
        myEmail = MyEmail()
        myEmail.build_connect()
        for i in range(10000):
            if i > 10: 
                notification = Notification()
                notification.local_beep()

            myEmail.activate()
            content = myEmail.get_spare()
            print(f'* waiting for email [{type}]...', content is not None)
            if content is not None:
                with open('log/email' + str(type) + '.yml', 'wb') as f:
                    print(content)
                    f.write(content)
                self.reload(type)
                break
            time.sleep(3)

    def once(self):
        try:
            response_yuepiao = self.poster.requests(1)
            response_tuijianpiao = self.poster.requests(2)
        except requests.exceptions.ProxyError:
            print('* cooldown...')
            return False
        
        if self.poster.check(1, response_yuepiao) == False:
            self.wait_email(1)
            return False
        
        if self.poster.check(2, response_tuijianpiao) == False:
            self.wait_email(2)
            return False

        # 获取最新红包日期，如果发现及时（检测时间小于20ms），就发送通知
        timestamp_yuepiao = response_yuepiao['Data']['HongbaoList']['Data'][0]['TimeOfCreateHongbao']
        str_time_yuepiao = TimeTransformer().timestamp2str_time(int(timestamp_yuepiao)/1000)
        residual_yuepiao = time.time() * 1000 - timestamp_yuepiao

        timestamp_tuijianpiao = response_tuijianpiao['Data']['HongbaoList']['Data'][0]['TimeOfCreateHongbao']
        str_time_tuijianpiao = TimeTransformer().timestamp2str_time(int(timestamp_tuijianpiao)/1000)
        residual_tuijianpiao = time.time() * 1000 - timestamp_tuijianpiao

        print(f"月票 {str_time_yuepiao}, 推荐票 {str_time_tuijianpiao}, now: {TimeTransformer().timestamp2str_time()}, residual_yuepiao: {residual_yuepiao}, residual_tuijianpiao: {residual_tuijianpiao}")

        if residual_yuepiao < 20 or residual_tuijianpiao < 20:
            return True
        return False

if __name__ == '__main__':
    mainPro = MainPro()
    mainPro.reload(1)
    mainPro.reload(2)
    notification = Notification()
    while True:
        if mainPro.once():
            notification.local()
        time.sleep(1)
        pass

    print('over')

