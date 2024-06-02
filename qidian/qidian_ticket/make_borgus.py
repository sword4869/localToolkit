from src.AdbSwipe import AdbSwipe
import time
import tqdm
from src.Expirations import Expirations
from src.TimeTransformer import TimeTransformer


if __name__ == '__main__':
    adbswipe = AdbSwipe()
    expirations = Expirations(TimeTransformer())
    expirations.recover()
    time.sleep(10)
    expirations.get_expirations(count=20)

    # 歇5秒，让你切换到shell，然后等待自动输入命令
    wait_count = 5
    with tqdm.tqdm(total=wait_count) as pbar:
        for i in range(wait_count):
            time.sleep(1)
            pbar.update(1)
    for expiration in tqdm.tqdm(expirations.expirations):
        expirations.big_clip(expiration)
        adbswipe.swipe_flush()
        time.sleep(1)

    expirations.recover()