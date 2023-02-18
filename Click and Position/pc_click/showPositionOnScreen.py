import cv2 as cv
import pyautogui as pg
import numpy as np
import time
import json
import keyboard

# 让左上角可以不退出
pg.FAILSAFE = False

# 相对位置
x, y = 0, 0

init_flag = True
x_positions = []
y_positions = []
times = []
while True:
    position = pg.position()
    text = '(%d,%d)' % (position[0]-x,position[1]-y)
    # print(text)
    img = np.zeros((50,200,3), np.uint8)
    cv.putText(img, text, (0,40), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv.LINE_AA)
    cv.imshow('position', img)
    cv.waitKey(1)

    # 按下esc退出 
    pressedKey = keyboard.read_key()
    if pressedKey == 27:
        data = {
            'x_position' : x_positions,
            'y_position' : y_positions,
            'time': times
        }
        with open("some.json", "w", encoding='utf-8') as f:
            json.dump(data, f)
        break
    # 打印坐标
    elif pressedKey == ord('g'):
        if init_flag:
            history_time = time.time()
            init_flag = False
        now_time = time.time()
        time_count = int(now_time - history_time)
        print(text, time_count)
        x_positions.append(position[0]-x)
        y_positions.append(position[1]-y)
        times.append(time_count)
        



'''

import cv2 as cv
import pyautogui as pg
import numpy as np
import time
import json
import keyboard

# 让左上角可以不退出
pg.FAILSAFE = False

# 相对位置
x, y = 0, 0
history_time = time.time()

def write_json(x_positions, y_positions, times):
    data = {
        'x_position' : x_positions,
        'y_position' : y_positions,
        'time': times
    }
    with open("some.json", "w", encoding='utf-8') as f:
        json.dump(data, f)

def flush_info(x_positions, y_positions, times):
    position = pg.position()
    text = '(%d,%d)' % (position[0]-x,position[1]-y)
    # print(text)
    img = np.zeros((50,200,3), np.uint8)
    cv.putText(img, text, (0,40), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv.LINE_AA)
    cv.imshow('position', img)
    cv.waitKey(1)
    now_time = time.time()
    time_count = int(now_time - history_time)
    print(text, time_count)
    x_positions.append(position[0]-x)
    y_positions.append(position[1]-y)
    times.append(time_count)


x_positions = []
y_positions = []
times = []

# 按下esc退出 
keyboard.add_hotkey('q', write_json, args=(x_positions, y_positions, times))
# 打印坐标
keyboard.add_hotkey('g', flush_info, args=(x_positions, y_positions, times))

'''