import winsound # windows
import time
import requests
import random


class Notification:
    def local_beep(self):
        ###
        # 本地发出声响
        ###
        duration = 2000  # millisecond  
        freq = 600  # Hz
        winsound.Beep(freq, duration)
        time.sleep(1)

    def local_alter(self):
        ###
        # 'SystemAsterisk', Asterisk

        # 'SystemExclamation', Exclamation

        # 'SystemExit', Exit Windows

        # 'SystemHand', Critical Stop

        # 'SystemQuestion', Question
        ###
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    
    def remote(self, title='ok', content=random.random()):
        ###
        # 微信 pushplus 公众号通知
        ###
        token = '' #在pushplus网站中可以找到
        title= title #改成你要的标题内容
        # content 还得变个花样，不然{"code":999,"msg":"请勿频繁推送相同内容","data":null}
        content = content #改成你要的正文内容
        url = 'http://www.pushplus.plus/send?token={}&title={}&content={}'.format(token, title, content)
        response = requests.get(url)
        # print(response.text)