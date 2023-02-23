import subprocess
from PIL import Image
import time


def swipe_flush():
    '''swipe screen to flush'''
    x1, y1, x2, y2, duration = 1050, 600, 1050, 1600, 500
    cmd = f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"
    subprocess.check_output(cmd, shell=True)


def get_screen():
    '''screen shot and upload'''
    cmds = [f'adb shell screencap -p /sdcard/1.png',
            'adb pull /sdcard/1.png',
            'adb shell rm /sdcard/1.png']
    for cmd in cmds:
        subprocess.check_output(cmd, shell=True)
    return Image.open('1.png').convert("RGB")


def discriminator(pos: tuple, img: Image, color: list):
    '''discriminator status'''
    color_now = img.getpixel(pos)
    print(color_now)
    return color != color_now


def click_bonus(pos: tuple):
    '''submit a ticket'''
    cmd = f'adb shell input tap {pos[0]} {pos[1]}'
    for i in range(3):
        subprocess.check_output(cmd, shell=True)
        time.sleep(0.3)


def close_failure(pos: tuple):
    cmd = f'adb shell input tap {pos[0]} {pos[1]}'
    subprocess.check_output(cmd, shell=True)


def train():
    while True:
        swipe_flush()
        time.sleep(1)
        img = get_screen()
        if discriminator(pos_status, img, color_true):
            continue
        img.show()
        click_bonus(pos_submit)
        close_failure(pos_other)


def test():
    import numpy as np
    import cv2 as cv
    # mouse callback function
    def draw_circle(event,x,y,flags,param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            cv.circle(img,(x,y),50,(255,0,0),-1)
            print(x,y)
            
    img = cv.imread('1.png')
    # height, width
    print(img.shape)
    cv.namedWindow('image', cv.WINDOW_GUI_NORMAL)
    cv.setMouseCallback('image',draw_circle)
    while(1):
        cv.imshow('image',img)
        if cv.waitKey(20) & 0xFF == 27:
            break
    cv.destroyAllWindows()


if __name__ == '__main__':
    import configargparse
    parser = configargparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='test()')
    parser.add_argument('--device', type=str, help='v,r')
    args = parser.parse_args()



    import yaml

    with open('pos.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if args.device == None:
        device_type = 'vivox9'
        # device_type = 'realmeq3pro'
    else:
        if args.device == 'v':
            device_type = 'vivox9'
        elif args.device == 'r':
            device_type = 'realmeq3pro'

    print(f'device_type = {device_type}')
    data = data[device_type]

    # 红色可抢
    color_true = eval(data['color_true'])
    # 红包记录的位置
    pos_status = eval(data['pos_status'])
    # 投票按钮
    pos_submit = eval(data['pos_submit'])
    # 空白退出
    pos_other = eval(data['pos_other'])

    if args.test:
        test()
    else:
        train()