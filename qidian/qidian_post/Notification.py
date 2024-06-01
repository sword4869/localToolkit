import winsound
import time
import requests
import random


class Notification:
    def local(self):
        duration = 2000  # millisecond  
        freq = 600  # Hz
        for _ in range(0,100):
            winsound.Beep(freq, duration)
            time.sleep(1)

    # content 还得变个花样，{"code":999,"msg":"请勿频繁推送相同内容","data":null}
    def remote(self, title='ok', content=random.random()):
        token = '6c17642c94fc46bd8e7cd71883ae820f' #在pushplus网站中可以找到
        title= title #改成你要的标题内容
        content = content #改成你要的正文内容
        url = 'http://www.pushplus.plus/send?token={}&title={}&content={}'.format(token, title, content)
        response = requests.get(url)
        # print(response.text)