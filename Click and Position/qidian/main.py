import subprocess
from PIL import Image
import time

# swipe screen to flush


def swipe_flush():
    x1, y1, x2, y2, duration = 1050, 600, 1050, 1600, 500
    cmd = f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"
    subprocess.check_output(cmd, shell=True)

# screen shot and upload


def get_screen():
    cmds = [f'adb shell screencap -p /sdcard/1.png',
            'adb pull /sdcard/1.png',
            'adb shell rm /sdcard/1.png']
    for cmd in cmds:
        subprocess.check_output(cmd, shell=True)
    return Image.open('1.png').convert("RGB")

# discriminator status


def discriminator(pos: tuple, img: Image, color: list):
    color_now = img.getpixel(pos)
    print(color_now)
    return color != color_now 

# submit a ticket


def click_bonus(pos: tuple):
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
        break


def test(pos: tuple):
    def paint_pos(pos: tuple, img: Image):
        pos_x, pos_y = pos[0], pos[1]
        for i in range(pos_x - 10, pos_x + 10):
            for j in range(pos_y - 10, pos_y + 10):
                img.putpixel((i, j), (0, 255, 0))

    img = Image.open('1.png').convert("RGB")
    color_now = img.getpixel(pos)
    print(color_now)
    paint_pos(pos, img)
    img.show()


if __name__ == '__main__':
    # # 有红包记录时, 已抢完状态的颜色
    # color_history = (224, 224, 224)
    # # 因为今日没有红包记录, 所以是背景色
    # color_blank = (245, 245, 245)
    # # 刷新中的背景色
    # color_blank2 = (255, 255, 255)

    # 红色可抢
    color_true = (229, 53, 62)

    # 热门活动
    pos_tabbar = (540, 350)

    # 红包记录的位置
    pos_status = (833, 833)
    # pos_status = (958, 696)

    # 投票按钮
    pos_submit = (533, 1400)

    pos_other = (900, 1700)

    train()
    # test(pos_status)
