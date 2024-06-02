###
# 即时版本。borgus过期就等邮件
###
from math import e
import os
import time
import requests
from PIL import Image

from src.Poster import Poster
from src.Notification import Notification
from src.MyEmail import MyEmail
from src.TimeTransformer import TimeTransformer
from src.GetHeader import GetHeader
from src.AdbSwipe import AdbSwipe

class MainPro:
    def __init__(self) -> None:
        self.getHeader = GetHeader()
        self.poster = Poster()
        
    def append_headers(self, type_files):
        headers_yuepiao = []
        headers_tuijianpiao = []
        for type, file in type_files:
            header = self.getHeader.load(file)
            if type == 'yuepiao':
                headers_yuepiao.append(header)
            elif type == 'tuijianpiao':
                headers_tuijianpiao.append(header)
        
        self.poster.reload_headers('yuepiao', headers_yuepiao)
        self.poster.reload_headers('tuijianpiao', headers_tuijianpiao)

    def wait_email(self):
        myEmail = MyEmail()
        myEmail.build_connect()
        for i in range(10000):
            if i > 10: 
                notification = Notification()
                notification.start_local_alter()

            myEmail.activate()
            contents = myEmail.get_contents()
            print(f'* waiting for email ...', len(contents) > 0)

            if len(contents) > 0:
                type_files = []
                for type, content in contents:
                    # 将content转化为lines
                    lines = content.decode('utf-8').split('\r\n')
                    lines = [line + '\n' for line in lines if line != '']
                    # 去掉第一行
                    lines = lines[1:]
                    # tstamp
                    tstamp = lines[3].split(': ')[1][:-1]
                    # 转化tstamp为时间字符串
                    tstamp_str = TimeTransformer().timestamp2str_time(int(tstamp)/1000, '%H%M%S')
                    with open(f'log/{type}/{tstamp}_{tstamp_str}.yml', 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    type_files.append([type, f'log/{type}/{tstamp}_{tstamp_str}.yml'])
                self.append_headers(type_files)
                break
            time.sleep(3)

    def once(self):
        try:
            response_yuepiao = self.poster.requests('yuepiao')
            response_tuijianpiao = self.poster.requests('tuijianpiao')
            with open('log/yuepiao_response.json', 'w', encoding='utf-8') as f:
                f.write(str(response_yuepiao))
            with open('log/tuijianpiao_response.json', 'w', encoding='utf-8') as f:
                f.write(str(response_tuijianpiao))
        except requests.exceptions.ProxyError:
            print('* cooldown...')
            return None
        except IndexError:
            if(self.poster.index_yuepiao >= len(self.poster.headers_yuepiao)):
                print('* [🚀yuepiao] waiting for email')
            if(self.poster.index_tuijianpiao >= len(self.poster.headers_tuijianpiao)):
                print('* [🌏tuijianpiao] waiting for email')
            self.wait_email()
            return None
        
        if self.poster.check('yuepiao', response_yuepiao) == False:
            print(f'* [🚀yuepiao] try next headers: {self.poster.index_yuepiao}/{len(self.poster.headers_yuepiao)}')
            self.poster.index_yuepiao += 1
            if self.poster.index_yuepiao >= len(self.poster.headers_yuepiao):
                print('* [🚀yuepiao] all headers have been tried')
                # 删除所有文件
                for file_name in os.listdir('log/yuepiao'):
                    os.remove(f'log/yuepiao/{file_name}')
                self.wait_email()
            return None
        
        if self.poster.check('tuijianpiao', response_tuijianpiao) == False:
            print(f'* [🌏tuijianpiao] try next headers: {self.poster.index_tuijianpiao}/{len(self.poster.headers_tuijianpiao)}')
            self.poster.index_tuijianpiao += 1
            if self.poster.index_tuijianpiao >= len(self.poster.headers_tuijianpiao):
                print('* [🌏tuijianpiao] all headers have been tried')
                # 删除所有文件
                for file_name in os.listdir('log/tuijianpiao'):
                    os.remove(f'log/tuijianpiao/{file_name}')
                self.wait_email()
            return None

        # 获取最新红包日期，如果发现及时（检测时间小于20ms），就发送通知
        timestamp_yuepiao = response_yuepiao['Data']['HongbaoList']['Data'][0]['TimeOfCreateHongbao']
        str_time_yuepiao = TimeTransformer().timestamp2str_time(int(timestamp_yuepiao)/1000)
        residual_yuepiao = time.time() * 1000 - timestamp_yuepiao

        timestamp_tuijianpiao = response_tuijianpiao['Data']['HongbaoList']['Data'][0]['TimeOfCreateHongbao']
        str_time_tuijianpiao = TimeTransformer().timestamp2str_time(int(timestamp_tuijianpiao)/1000)
        residual_tuijianpiao = time.time() * 1000 - timestamp_tuijianpiao

        print(f"月票 {str_time_yuepiao}, 推荐票 {str_time_tuijianpiao}, now: {TimeTransformer().timestamp2str_time()}, residual_yuepiao: {int(residual_yuepiao//1000)}, residual_tuijianpiao: {int(residual_tuijianpiao//1000)}")

        if residual_yuepiao < 10000:
            return 'yuepiao'
        elif residual_tuijianpiao < 10000:
            return 'tuijianpiao'
        return None

    def logger(self, headers):
        header_str_time = TimeTransformer().timestamp2str_time(int(headers['tstamp'])/1000)

        with open('log/log.txt', 'a', encoding='utf-8') as f:
            line = f"{headers['borgus']},{headers['tstamp']},{header_str_time}\n"
            f.write(line)

if __name__ == '__main__':
    notification = Notification()
    mainPro = MainPro()
    adbswipe = AdbSwipe()
    show_img = Image.open(f'log/1.png')

    # list files in log/yuepiao, log/tuijianpiao
    type_files = []
    for file_name in os.listdir('log/yuepiao'):
        type_files.append(['yuepiao', f'log/yuepiao/{file_name}'])
    for file_name in os.listdir('log/tuijianpiao'):
        type_files.append(['tuijianpiao', f'log/tuijianpiao/{file_name}'])
    mainPro.append_headers(type_files) 

    while True:
        type = mainPro.once() 
        if type is not None:
            print(f'* [{type}] trigger', time.strftime("%H:%M:%S", time.localtime()))
            notification.start_local_beep()
            show_img.show()
            try:
                if(type == 'yuepiao'):
                    adbswipe.tap(adbswipe.POS_MONTH)
                elif(type == 'tuijianpiao'):
                    adbswipe.tap(adbswipe.POS_RECOMMEND)
                adbswipe.swipe_flush()
                adbswipe.click_bonus()
                adbswipe.swipe_flush()
            except Exception as e:
                print('* [adb] swipe_flush or click_bonus error')
        time.sleep(1)
        pass