import subprocess
from PIL import Image
import time


def swipe_flush():
    x1, y1, x2, y2, duration = 1050, 600, 1050, 1600, 500
    cmd = f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"
    subprocess.run(cmd, shell=True)


def get_screen():
    cmds = [f'adb shell screencap -p /sdcard/1.png',
           'adb pull /sdcard/1.png',
           'adb shell rm /sdcard/1.png']
    for cmd in cmds:
        subprocess.run(cmd, shell=True)
    return Image.open('1.png').convert("RGB")
    
def discriminator(img: Image):
    pos_x, pos_y = 833, 833
    color_history = (224, 224, 224)
    # for i in range(pos_x -10, pos_x + 10):
    #     for j in range(pos_y - 10, pos_y + 10):
    #         img.putpixel((i, j), (255, 255, 0))
    # img.show()
    color = img.getpixel((pos_x, pos_y))
    print(color)
    assert color_history == color

if __name__ == '__main__':
    while True:
        swipe_flush()
        time.sleep(1)
        img = get_screen()
        try: 
            discriminator(img)
        except:
            img.show()
            break