import subprocess
import time

def swipe_flush():
    '''swipe screen to flush'''
    x1, y1, x2, y2, duration = 1050, 600, 1050, 1600, 500
    cmd = f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"
    subprocess.check_output(cmd, shell=True)

for i in range(10000):
    swipe_flush()
    time.sleep(10)
    print(f"swipe {i} times")