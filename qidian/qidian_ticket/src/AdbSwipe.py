import subprocess
import time
import cv2
import yaml
import configargparse
from PIL import Image

class AdbSwipe:
    def __init__(self):
        with open('config/pos.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        DEVICE_TYPE = data['device_type']
        data_device = data[DEVICE_TYPE]

        # 红色可抢
        self.COLOR_TRUE = eval(data_device['color_true'])
        # 红包记录的位置
        self.POS_STATUS = eval(data_device['pos_status'])
        # 投票按钮
        self.POS_SUBMIT = eval(data_device['pos_submit'])
        # 月票按钮
        self.POS_MONTH = eval(data_device['pos_month'])
        # 推荐票按钮
        self.POS_RECOMMEND = eval(data_device['pos_recommend'])
        # 空白退出
        self.POS_OTHER = eval(data_device['pos_other'])
        # 缩小显示
        self.RESIZE = data_device['resize']

        self.SLEEP_MS = data['sleep_ms']

        parser = configargparse.ArgumentParser()
        parser.add_argument('-s', '--sleep_ms', type=int, default=None)
        args = parser.parse_args()

        if args.sleep_ms:
            self.SLEEP_MS = args.sleep_ms

    def tap(self, pos: tuple):
        '''tap screen'''
        cmd = f'adb shell input tap {pos[0]} {pos[1]}'
        subprocess.check_output(cmd, shell=True)

    def swipe_flush(self):
        '''swipe screen to flush'''
        x1, y1, x2, y2, duration = 1050, 600, 1050, 1600, 100
        cmd = f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"
        subprocess.check_output(cmd, shell=True)

    def screenshot(self, save_path):
        '''screen shot and upload'''
        file_path = f'{save_path}/1.png'
        cmds = [
            'adb shell screencap -p /sdcard/1.png',
            f'adb pull /sdcard/1.png {file_path}',
            'adb shell rm /sdcard/1.png'
        ]
        for cmd in cmds:
            subprocess.check_output(cmd, shell=True)
        return Image.open(file_path).convert("RGB")


    def discriminator(self, pos: tuple, COLOR_TRUE: tuple, cv_img, gui=False):
        '''discriminator status'''
        color_now = cv_img[pos[1], pos[0]]
        color_now = tuple(color_now[::-1].tolist())
        
        if gui:
            cv2.putText(cv_img, str(color_now), (pos[0] - 300, pos[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(cv_img, str(COLOR_TRUE), (pos[0] - 300, pos[1] + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            print(color_now)
        return COLOR_TRUE == color_now


    def click_bonus(self):
        '''submit a ticket'''
        self.tap(self.POS_STATUS)
        self.tap(self.POS_STATUS)
        time.sleep(0.5)
        for i in range(3):
            self.tap(self.POS_SUBMIT)
            time.sleep(0.3)


    def close_failure(self, pos: tuple):
        cmd = f'adb shell input tap {pos[0]} {pos[1]}'
        subprocess.check_output(cmd, shell=True)

    def callback_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_FLAG_LBUTTON:
            x = x * self.RESIZE
            y = y * self.RESIZE
            print(f'click {x} {y}')
            self.tap((x, y))
        if event == cv2.EVENT_FLAG_RBUTTON:
            time.sleep(5)
            