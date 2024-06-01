import json
from turtle import pos

import requests
import urllib3


# for InsecureRequestWarning
urllib3.disable_warnings()

class Poster:
    def __init__(self) -> None:
        self.my_url = 'https://druidv6.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?lastHongbaoId=0&pn=1&pz=20&type='
        self.body = {}
        self.headers = [None, None]

    def reload_headers(self, headers, type):
        self.headers[type - 1] = headers

    def requests(self, type):
        # type = 1: 月票, 2: 推荐票
        response = requests.get(
            url=self.my_url + str(type), data=self.body, headers=self.headers[type - 1], verify=False)
        
        jsonData = json.loads(response.text)
        # print(jsonData)
        with open("log/" + str(type) + ".json", "w", encoding='utf-8') as f:
            json.dump(jsonData, f)

        return jsonData

    def check(self, type, jsonData) -> bool:
        '''
        成功：{"Result": 0, ...}
        
        失败：{'Result': -3, 'Message': '参数错误'}
        '''
        if jsonData['Result'] != 0:
            print(f'* post failure {type}: {jsonData}')
            return False
        else:
            return True
    pass