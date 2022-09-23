#!usr/bin/env python3
import pyautogui as pg
import time
# 需要用sys.argv[1:]参数
import sys
import getopt


def clickCenter(center, clicks=1, button='left', interval=0.0):
    pg.click(phoneTopLeftPosition[0] + center[0],
             phoneTopLeftPosition[1] + center[1],
             clicks=clicks,
             button=button,
             interval=interval)


def moveCenter(center):
    pg.moveTo(phoneTopLeftPosition[0] + center[0],
              phoneTopLeftPosition[1] + center[1])


def imgCenter(imgName=None, modeException=True):
    if imgName == None:
        raise Exception('imgCenterClickLackFileName')

    center = pg.locateCenterOnScreen(imgName)
    if center != None:
        return center
    else:
        if modeException == True:
            raise Exception('imgCenterClickNoneCenter')
        else:
            return None


def openHome():
    phoneCenter = pg.center(region)
    pg.click(phoneCenter[0],
             phoneCenter[1],
             clicks=2,
             interval=1,
             button='middle')


def homePage(direction='l'):
    pointLeft = (phoneTopLeftPosition[0] + 100,
                 phoneButtomRightPosition[1] - 300)
    pointRight = (phoneButtomRightPosition[0] - 100,
                  phoneButtomRightPosition[1] - 300)

    if direction == 'l':
        pg.moveTo(pointLeft[0], pointLeft[1])
        pg.dragTo(pointRight[0], pointRight[1])
    else:
        pg.moveTo(pointRight[0], pointRight[1])
        pg.dragTo(pointLeft[0], pointLeft[1])


def openAlipay():
    # home
    time.sleep(2)
    openHome()

    # 翻页
    time.sleep(2)
    for _ in range(2):
        homePage('r')

    # Open
    time.sleep(2)
    clickCenter((347, 84))


def openTaobao():
    openHome()

    # 翻页
    time.sleep(3)
    for _ in range(2):
        homePage('r')

    # 淘宝
    time.sleep(3)
    clickCenter((90, 85))

    # 巴巴农场
    time.sleep(5)
    clickCenter((176, 474))


def baba_field():
    # 立即去收
    pos = (286, 817)
    clickCenter(pos)
    time.sleep(2)

    # 农田1 2 3 4 5
    points = [(288, 762), (182, 699), (279, 641), (177, 567), (393, 571)]

    for i in points:
        clickCenter(i)
        time.sleep(2)
        clickCenter(pos)


def baba_sun():
    # 阳光
    points2 = [(93, 454), (224, 499), (189, 391), (282, 425), (372, 503),
               (302, 318), (407, 371), (504, 450)]

    # x关闭
    pos = (286, 817)

    for _ in range(10):
        for i in points2:
            clickCenter(i)
            clickCenter(pos)


def baba_orange():
    for _ in range(3):
        # 去逛逛
        clickCenter((474, 621))
        time.sleep(20)

        # 返回<
        clickCenter((49, 65))
        time.sleep(2)


if __name__ == '__main__':
    # res = pg.confirm(buttons=['Alipay', 'Pass'])
    # if res == 'Alipay':
    #     openAlipay()
    #     AntForest()
    # else:
    #     pass

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

    phoneTopLeftPosition = (int(x), int(y))
    # width x height
    phoneSize = (559, 990)
    phoneButtomRightPosition = (phoneTopLeftPosition[0] + phoneSize[0],
                                phoneTopLeftPosition[1] + phoneSize[1])

    region = (phoneTopLeftPosition[0], phoneTopLeftPosition[1], phoneSize[0],
              phoneSize[1])

    pg.PAUSE = 0.5

    while True:
        functions = [
            'home', 'openTaobao', 'openAlipay', 'baba_field', 'baba_sun',
            'baba_orange', 'exit'
        ]
        res = pg.confirm(buttons=functions)
        if res == functions[0]:
            openHome()
        elif res == functions[1]:
            openTaobao()
        elif res == functions[2]:
            openAlipay()
        elif res == functions[3]:
            baba_field()
        elif res == functions[4]:
            baba_sun()
        elif res == functions[5]:
            baba_orange()
        elif res == functions[6]:
            break
        else:
            raise Exception('main_function_notFound')
