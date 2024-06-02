from certifi import contents
from imapclient import IMAPClient       # pip install imapclient
import email

class MyEmail:
    def __init__(self) -> None:
        self.server_host = 'imap.163.com'
        self.username = 'sandal33s@163.com'    
        self.password = 'LJJFBAQEMNUCEAIZ'  # 授权码 

    def build_connect(self):
        self.server = IMAPClient(self.server_host)
        self.server.login(self.username, self.password)
        # 163邮箱，采用新版email标准，需要提供id，随便写
        self.server.id_({"name": "IMAPClient", "version": "2.1.0"})

    def activate(self):
        """确保激活"""
        try:
            self.server.select_folder('INBOX')
            self.server.search("UNSEEN")
        except ConnectionAbortedError as e:
            # 如果出现掉线的情况，那么重连
            self.build_connect()

    def get_contents(self, filter=True):
        contents = []

        # 收信箱
        self.server.select_folder('INBOX')
        # 查看未读邮件，下面fetch()后自动标记为已读，就不会重复。
        messages = self.server.search("UNSEEN")
        # 遍历每封邮件，我们只需要最新的一封
        for uid, message_data in self.server.fetch(messages, "RFC822").items():
            # 转为email对象
            message = email.message_from_bytes(message_data[b"RFC822"])
            # 各种payload，正文、附件、图片
            multipart_payload = message.get_payload()
            for sub_message in multipart_payload:
                # 原本能只发响应，对应 text/plain；
                # 现在小黄鸟出问题，只能都发两个附件，对应 application/octet-stream
                # print(sub_message.get_content_type())
                # multipart/alternative
                # application/octet-stream
                # application/octet-stream
                if sub_message.get_content_type() == 'application/octet-stream':
                    # The actual text/HTML email contents, or attachment data
                    content = sub_message.get_payload(decode=True)  # 字节
                    
                    if filter:
                        if content.startswith(b'GET /Atom.axd/Api/HongBao/GetSquare?lastHongbaoId=0&pn=1&pz=20&type=1'):
                            contents.append(['yuepiao', content])
                        elif content.startswith(b'GET /Atom.axd/Api/HongBao/GetSquare?lastHongbaoId=0&pn=1&pz=20&type=2'):
                            contents.append(['tuijianpiao', content])
                    else:
                        contents.append(content)
        return contents

if __name__ == '__main__':
    myEmail = MyEmail()
    myEmail.build_connect()
    myEmail.activate()
    content = myEmail.get_spare()
    print('* waiting for email...', content is not None)
    print(content)
