import time

import pyautogui as pg
import tqdm

from src.MyEmail import MyEmail
from src.TimeTransformer import TimeTransformer


class MakePartHeaders:

    def __init__(self) -> None:
        self.timeTransformer = TimeTransformer()

    def get_expirations(self, count=1):
        # 当前时间
        now_str_time = self.timeTransformer.timestamp2str_time()
        print(f'now : {now_str_time}')


        # 选择有效的时间段
        self.expirations = []
        bias = 900
        for i in range(count):
            # formulation：十五分钟一次
            next_expiration_timestamp = bias + int(int(time.time()) / 900) * 900 + 900 * i
            next_expiration_str_time = self.timeTransformer.timestamp2str_time(next_expiration_timestamp, '%H:%M:%S')
            print(next_expiration_str_time)

            self.expirations.append(next_expiration_str_time)

        print(self.expirations)



    def big_clip(self, str_time):
        def small_clip(cmd):
            pg.typewrite(cmd)
            pg.press('enter')

        small_clip(f"date '{str_time}'")
        small_clip('exit')
        small_clip('su')


    def work_phone(self):

        time.sleep(5)

        for expiration in self.expirations:
            self.big_clip(expiration)

            wait_count = 20
            with tqdm.tqdm(total=wait_count) as pbar:
                for i in range(wait_count):
                    pbar.set_description(expiration)
                    time.sleep(1)
                    pbar.update(1)

    def recover(self):
        time.sleep(5)

        right_time = self.timeTransformer.struct_time2str_time()
        print(right_time)
        self.big_clip(right_time)


if __name__ == '__main__':

    def make_borgus():
        makePartHeaders = MakePartHeaders()
        makePartHeaders.get_expirations(count=20)
        makePartHeaders.work_phone()
        makePartHeaders.recover()

    def parse_email():

        myEmail = MyEmail()
        myEmail.build_connect()
        content = myEmail.get_spare()

        with open('log/spare.txt', 'wb') as f:
            f.write(content)

    def while_ans(hint, func):
        while True:
            ans = input(hint)
            if ans == 'y':
                func()
            elif ans == 'n':
                break
            else:
                pass

    while_ans('* make borgus and tstamp?(y/n)', make_borgus)
    while_ans('* wait email?(y/n)', parse_email)