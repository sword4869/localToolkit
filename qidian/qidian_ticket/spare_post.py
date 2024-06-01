import http
import time

import requests

from src.GetHeaders import GetHeaders
from src.Notification import Notification
from src.Poster import Poster
from src.TimeTransformer import TimeTransformer


class ExceptionCooldown(Exception):
    pass

class MainPro:
    def __init__(self, part_headers) -> None:
        
        self.poster = Poster()
        self.GetHeaders = GetHeaders()
        
        headers = self.GetHeaders.load()
        self.poster.reload_headers(headers)

        self.index = 0
        self.part_headers = part_headers

        self.fp = open('log/crital.txt', 'a')

    def once(self):
        now_str_time = TimeTransformer().timestamp2str_time()

        try:
            print(f'\r* start request, {now_str_time}', end=' ')
            self.poster.requests()
        except requests.exceptions.ProxyError:
            print(f'* requests.exceptions.ProxyError {now_str_time}', file=self.fp)
            raise ExceptionCooldown()
        except requests.exceptions.ConnectionError:
            print(f'* requests.exceptions.ConnectionError {now_str_time}', file=self.fp)
            raise ExceptionCooldown()
        except http.client.RemoteDisconnected:
            print(f'* http.client.RemoteDisconnected {now_str_time}', file=self.fp)
            raise ExceptionCooldown()
        print(f'* finish request', end=' ')

        
        if self.poster.check() == False:
            headers = self.GetHeaders.load()
            headers['tstamp'] = self.part_headers[self.index]
            headers['borgus'] = self.part_headers[self.index+1]
            self.index += 2
            self.poster.reload_headers(headers)

            new_ts_str_time = int(headers['tstamp'])/1000
            print(f"new tstamp: {headers['tstamp']},  {TimeTransformer().timestamp2str_time(new_ts_str_time)}, now = {now_str_time}", file=self.fp)

            return

        timestamp = self.poster.jsonData['Data']['HongbaoList']['Data'][0]['TimeOfCreateHongbao']
        str_time = TimeTransformer().timestamp2str_time(int(timestamp)/1000)
        print(f"红包日期 {str_time}", end=' ')

        residual = time.time() * 1000 - timestamp
        if residual < 20:
            print(f'* residual: {residual}, {now_str_time}', file=self.fp)
            raise Exception('Quick')

        self.fp.flush()

if __name__ == '__main__':

    with open('log/spare.txt', 'r') as f:
        lines = f.readlines()

    part_headers = []
    for i in lines:
        if i == '\n':
            continue
        part_headers.append(i[:-1])
    print(part_headers)

    notification = Notification()
    mainPro = MainPro(part_headers)
    while True:
        try:
            mainPro.once()
        except ExceptionCooldown:
            notification.local_alter()
        except Exception as e:
            print(type(e))
            print(e)
            notification.local_beep()
        time.sleep(1)
        pass

    print('over')
