import subprocess
from PIL import Image
import time
import cv2
import numpy as np
import yaml

def swipe_flush():
    '''swipe screen to flush'''
    x1, y1, x2, y2, duration = 1050, 600, 1050, 1600, 500
    cmd = f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"
    subprocess.check_output(cmd, shell=True)


def screenshot():
    '''screen shot and upload'''
    cmds = [f'adb shell screencap -p /sdcard/1.png',
            'adb pull /sdcard/1.png',
            'adb shell rm /sdcard/1.png']
    for cmd in cmds:
        subprocess.check_output(cmd, shell=True)


def discriminator(pos: tuple, color_true: tuple, cv_img, gui=False):
    '''discriminator status'''
    color_now = cv_img[pos[1], pos[0]]
    color_now = tuple(color_now[::-1].tolist())
    text = str(color_now)
    
    if gui:
        cv2.putText(cv_img, text, (pos[0] - 300, pos[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    else:
        print(color_now)
    return color_true == color_now


def click_bonus(pos: tuple):
    '''submit a ticket'''
    cmd = f'adb shell input tap {pos[0]} {pos[1]}'
    for i in range(3):
        subprocess.check_output(cmd, shell=True)
        time.sleep(0.3)


def close_failure(pos: tuple):
    cmd = f'adb shell input tap {pos[0]} {pos[1]}'
    subprocess.check_output(cmd, shell=True)


def run(gui=False):
    i = 0
    while True:
        swipe_flush()
        time.sleep(1)
        screenshot()

        if gui is False:
            time.sleep(sleep_second)
        img = Image.open('1.png')

        discriminate = False
        if gui:
            cv_img = np.array(img)
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

            # 检测颜色
            discriminate = discriminator(pos_status, color_true, cv_img, gui)

            # 标注位置
            cv2.circle(cv_img, pos_status, 5, (0, 0, 255), -1)
            cv2.rectangle(cv_img, (pos_status[0] - 20, pos_status[1] - 40), (pos_status[0] + 100, pos_status[1] + 40), (0, 255, 0), 4)

            # 表示更新变化
            i += 100
            i = i % cv_img.shape[1]
            cv2.line(cv_img, (0,0),(i,0),(255,0,0),5)
            current_time = time.strftime("%H:%M:%S", time.localtime())
            cv2.putText(cv_img, current_time, (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 0), 3)

            # 缩小显示
            cv_img = cv2.resize(cv_img, (cv_img.shape[1]//3, cv_img.shape[0]//3), interpolation=cv2.INTER_AREA)
            cv2.imshow('image', cv_img)
            if cv2.waitKey(sleep_second * 1000) == ord('q'):
                break
        if discriminate is False:
            continue
        img.show()
        click_bonus(pos_submit)
        close_failure(pos_other)

def debug():
    # mouse callback function
    def draw_circle(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(img,(x,y),50,(255,0,0),-1)
            print(x,y)
            
    img = cv2.imread('1.png')
    # height, width
    print(img.shape)
    cv2.namedWindow('image', cv2.WINDOW_GUI_NORMAL)
    cv2.setMouseCallback('image',draw_circle)
    while(1):
        cv2.imshow('image',img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':

    with open('pos.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    device_type = data['device_type']
    data_device = data[device_type]

    # 红色可抢
    color_true = eval(data_device['color_true'])
    # 红包记录的位置
    pos_status = eval(data_device['pos_status'])
    # 投票按钮
    pos_submit = eval(data_device['pos_submit'])
    # 空白退出
    pos_other = eval(data_device['pos_other'])

    sleep_second = data['sleep_second']

    if data['debug']:
        debug()
    else:
        run(gui=True)