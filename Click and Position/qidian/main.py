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
def discriminator(pos:tuple, img: Image):
    color_history = (224, 224, 224)
    color = img.getpixel(pos)
    print(color)
    return color_history == color

# submit a ticket
def click_bonus(pos:tuple):
    cmd = f'adb shell input tap {pos[0]} {pos[1]}'
    subprocess.check_output(cmd, shell=True)

def show_pos(pos:tuple, img:Image):
    pos_x, pos_y = pos[0], pos[1]
    for i in range(pos_x -10, pos_x + 10):
        for j in range(pos_y - 10, pos_y + 10):
            img.putpixel((i, j), (255, 255, 255))
    img.show()

def train():
    pos_status = (833, 833)
    pos_submit = (533, 1400)
    while True:
        swipe_flush()
        time.sleep(1)
        img = get_screen()
        if discriminator(pos_status, img):
            continue
        click_bonus(pos_submit)

def test():
    pos = (533, 1400)
    img = Image.open('1.png').convert("RGB")
    show_pos(pos, img)

if __name__ == '__main__':
    train()
    # test()