import json
import requests
import urllib3

# for InsecureRequestWarning
urllib3.disable_warnings()

class Poster:
    def __init__(self) -> None:
        self.my_url = 'https://druidv6.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?lastHongbaoId=0&pn=1&pz=20&type='
        self.body = {}
        self.headers_yuepiao = []
        self.headers_tuijianpiao = []
        # index
        self.index_yuepiao = 0
        self.index_tuijianpiao = 0

    def reload_headers(self, type, headers):
        if type == 'yuepiao':
            self.headers_yuepiao += headers
        elif type == 'tuijianpiao':
            self.headers_tuijianpiao += headers

    def requests(self, type):
        if type == 'yuepiao':
            url = self.my_url + '1'
            headers = self.headers_yuepiao[self.index_yuepiao]
        elif type == 'tuijianpiao':
            url = self.my_url + '2'
            headers = self.headers_tuijianpiao[self.index_tuijianpiao]
        
        response = requests.get(url=url, data=self.body, headers=headers, verify=False)
        
        jsonData = json.loads(response.text)
        # print(jsonData)
        return jsonData

    def check(self, type, jsonData) -> bool:
        '''
        成功：{"Result": 0, ...}
        
        失败：{'Result': -3, 'Message': '参数错误'}
        '''
        if jsonData['Result'] == 0:
            return True
        
        print(f'* [{type}] post failure: {jsonData}')
        return False
