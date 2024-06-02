import time
import pyautogui as pg
import tqdm

class Expirations:

    def __init__(self, timeTransformer) -> None:
        self.timeTransformer = timeTransformer

    def get_expirations(self, count=1):
        # 当前时间
        now_str_time = self.timeTransformer.timestamp2str_time()
        # 选择有效的时间段
        self.expirations = []
        bias = 1800  # formulation：30分钟一次
        for i in range(count):
            next_expiration_timestamp = int(int(time.time()) / bias) * bias + bias * (i+1)
            next_expiration_str_time = self.timeTransformer.timestamp2str_time(next_expiration_timestamp, '%H:%M:%S')
            self.expirations.append(next_expiration_str_time)
        print(f'now : {now_str_time}', self.expirations)

    def big_clip(self, str_time):
        def small_clip(cmd):
            pg.typewrite(cmd)
            pg.press('enter')

        small_clip(f"date '{str_time}'")
        small_clip('exit')
        small_clip('su')

    def recover(self):
        wait_count = 5
        with tqdm.tqdm(total=wait_count) as pbar:
            for i in range(wait_count):
                time.sleep(1)
                pbar.update(1)
                
        right_time = self.timeTransformer.struct_time2str_time()
        print(right_time)
        self.big_clip(right_time)


