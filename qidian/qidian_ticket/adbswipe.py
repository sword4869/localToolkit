from src.AdbSwipe import AdbSwipe
import time
import cv2
import numpy as np

def run(adbswipe, gui=False):
    i = 0
    cv2.namedWindow('image', cv2.WINDOW_GUI_NORMAL)
    cv2.setMouseCallback('image', adbswipe.callback_click)
    while True:
        img = adbswipe.screenshot('log')
        adbswipe.swipe_flush()

        discriminate = False
        if gui:
            cv_img = np.array(img)
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

            # 检测颜色
            discriminate = adbswipe.discriminator(adbswipe.POS_STATUS, adbswipe.COLOR_TRUE, cv_img, gui)

            # 标注位置
            cv2.circle(cv_img, adbswipe.POS_STATUS, 5, (0, 0, 255), -1)
            cv2.rectangle(cv_img, (adbswipe.POS_STATUS[0] - 20, adbswipe.POS_STATUS[1] - 40), (adbswipe.POS_STATUS[0] + 100, adbswipe.POS_STATUS[1] + 40), (0, 255, 0), 4)

            # 表示更新变化
            i += 100
            i = i % cv_img.shape[1]
            cv2.line(cv_img, (0,0),(i,0),(255,0,0),5)
            current_time = time.strftime("%H:%M:%S", time.localtime())
            cv2.putText(cv_img, current_time, (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 0), 3)

            # 缩小显示
            cv_img = cv2.resize(cv_img, (cv_img.shape[1]// adbswipe.RESIZE, cv_img.shape[0]// adbswipe.RESIZE), interpolation=cv2.INTER_AREA)
            cv2.imshow('image', cv_img)
            if cv2.waitKey(adbswipe.SLEEP_MS) == ord('q'):
                break
        else:
            time.sleep(adbswipe.SLEEP_MS // 1000)

        if discriminate:
            print('trigger', time.strftime("%H:%M:%S", time.localtime()))
            adbswipe.click_bonus()
            adbswipe.swipe_flush()
            img.show()
            adbswipe.swipe_flush()

            # 发现不需要关闭，直接在边角点击即可关闭。而下滑刷新恰好就是点击边角
            # close_failure(POS_OTHER)

def debug():
    # mouse callback function
    def draw_circle(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(img,(x,y),50,(255,0,0),-1)
            print(x,y)
            
    img = cv2.imread('log/1.png')
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

    # debug()
    adbswipe = AdbSwipe()
    run(adbswipe, gui=True)