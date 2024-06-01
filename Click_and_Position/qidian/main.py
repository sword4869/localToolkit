import subprocess
from PIL import Image
import time
import cv2
import numpy as np
import yaml
import configargparse

def swipe_flush():
    '''swipe screen to flush'''
    x1, y1, x2, y2, duration = 1050, 600, 1050, 1600, 100
    cmd = f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"
    subprocess.check_output(cmd, shell=True)


def screenshot():
    '''screen shot and upload'''
    cmds = [f'adb shell screencap -p /sdcard/1.png',
            'adb pull /sdcard/1.png',
            'adb shell rm /sdcard/1.png']
    for cmd in cmds:
        subprocess.check_output(cmd, shell=True)


def discriminator(pos: tuple, COLOR_TRUE: tuple, cv_img, gui=False):
    '''discriminator status'''
    color_now = cv_img[pos[1], pos[0]]
    color_now = tuple(color_now[::-1].tolist())
    
    if gui:
        cv2.putText(cv_img, str(color_now), (pos[0] - 300, pos[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(cv_img, str(COLOR_TRUE), (pos[0] - 300, pos[1] + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        print(color_now)
    return COLOR_TRUE == color_now


def click_bonus(pos: tuple):
    '''submit a ticket'''
    cmd = f'adb shell input tap {pos[0]} {pos[1]}'
    for i in range(3):
        subprocess.check_output(cmd, shell=True)
        time.sleep(0.3)


def close_failure(pos: tuple):
    cmd = f'adb shell input tap {pos[0]} {pos[1]}'
    subprocess.check_output(cmd, shell=True)

def callback_click(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        x = x * RESIZE
        y = y * RESIZE
        print(f'click {x} {y}')
        cmd = f'adb shell input tap {x} {y}'
        subprocess.check_output(cmd, shell=True)
    if event == cv2.EVENT_FLAG_RBUTTON:
        time.sleep(5)
        
def run(gui=False):
    i = 0
    cv2.namedWindow('image', cv2.WINDOW_GUI_NORMAL)
    cv2.setMouseCallback('image', callback_click)
    while True:
        screenshot()
        swipe_flush()
        img = Image.open('1.png')

        discriminate = False
        if gui:
            cv_img = np.array(img)
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

            # 检测颜色
            discriminate = discriminator(POS_STATUS, COLOR_TRUE, cv_img, gui)

            # 标注位置
            cv2.circle(cv_img, POS_STATUS, 5, (0, 0, 255), -1)
            cv2.rectangle(cv_img, (POS_STATUS[0] - 20, POS_STATUS[1] - 40), (POS_STATUS[0] + 100, POS_STATUS[1] + 40), (0, 255, 0), 4)

            # 表示更新变化
            i += 100
            i = i % cv_img.shape[1]
            cv2.line(cv_img, (0,0),(i,0),(255,0,0),5)
            current_time = time.strftime("%H:%M:%S", time.localtime())
            cv2.putText(cv_img, current_time, (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 0), 3)

            # 缩小显示
            cv_img = cv2.resize(cv_img, (cv_img.shape[1]// RESIZE, cv_img.shape[0]// RESIZE), interpolation=cv2.INTER_AREA)
            cv2.imshow('image', cv_img)
            if cv2.waitKey(SLEEP_MS) == ord('q'):
                break
        else:
            time.sleep(SLEEP_MS // 1000)

        if discriminate:
            print('trigger', time.strftime("%H:%M:%S", time.localtime()))
            click_bonus(POS_SUBMIT)
            swipe_flush()
            img.show()

            # 发现不需要关闭，直接在边角点击即可关闭。而下滑刷新恰好就是点击边角
            # close_failure(POS_OTHER)

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

    DEVICE_TYPE = data['device_type']
    data_device = data[DEVICE_TYPE]

    # 红色可抢
    COLOR_TRUE = eval(data_device['color_true'])
    # 红包记录的位置
    POS_STATUS = eval(data_device['pos_status'])
    # 投票按钮
    POS_SUBMIT = eval(data_device['pos_submit'])
    # 空白退出
    POS_OTHER = eval(data_device['pos_other'])
    # 缩小显示
    RESIZE = data_device['resize']

    SLEEP_MS = data['sleep_ms']

    parser = configargparse.ArgumentParser()
    parser.add_argument('-s', '--sleep_ms', type=int, default=None)
    args = parser.parse_args()

    if args.sleep_ms:
        SLEEP_MS = args.sleep_ms

    if data['debug']:
        debug()
    else:
        run(gui=True)