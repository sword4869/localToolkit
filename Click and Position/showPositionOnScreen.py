import cv2 as cv
import pyautogui as pg
import numpy as np

# 需要用sys.argv[1:]参数
import sys
import getopt

print(sys.argv)

try:
	# 三种参数,help(h),username(u),password(p)。第一个不需要值，另外两个需要值
    opts, args = getopt.getopt(sys.argv[1:], "x:y:", ["x=", "y="])
    x = 0
    y = 0
    # 就是处理每个元组
    for k, v in opts:
        if k in ("-x", "--x"):
            x = v
        elif k in ("-y", "--y"):
            y = v
# 报错是getopt.GetoptError
except getopt.GetoptError:
    print('[getopt.GetoptError]')
    sys.exit()

# 左上角可以不退出
pg.FAILSAFE = False

while True:
    position = pg.position()
    text = '(%d,%d)' % (position[0]-int(x),position[1]-int(y))
    # print(text)
    img = np.zeros((50,200,3), np.uint8)
    cv.putText(img, text, (0,40), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv.LINE_AA)
    cv.imshow('position', img)
    if cv.waitKey(1) == 27:
        break
	
