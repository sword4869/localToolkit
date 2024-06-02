import json
import sys
import requests
import urllib3
import yaml

# for InsecureRequestWarning
urllib3.disable_warnings()

class GetHeader:
    def __init__(self) -> None:
        pass

    def load(self, file, use_origin=False):
        header = {
            'User-Agent': 'Mozilla/mobile QDReaderAndroid',
            'Host': 'druidv6.if.qidian.com'
        }
        try:
            with open(file) as f:
                origin_data = yaml.safe_load(f)
                origin_data['tstamp'] = str(origin_data['tstamp'])
        except Exception as e:
            print(f'* load header error: {e}')
            sys.exit(1)

        header['borgus'] = origin_data['borgus']
        header['tstamp'] = origin_data['tstamp']
        header['Cookie'] = origin_data['Cookie']

        if use_origin:
            return origin_data
        else:
            return header
    
if __name__ == '__main__':
    getHeader = GetHeader()
    header = getHeader.load(r'D:\code_my\localToolkit\qidian\qidian_ticket\log\tuijianpiao\1717324464901_183424.yml')   # 推荐
    # header = getHeader.load(r'D:\code_my\localToolkit\qidian\qidian_ticket\log\yuepiao\1717324462498_183422.yml')   # 月票

    url = 'https://druidv6.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?lastHongbaoId=0&pn=1&pz=20&type=1'
    url = 'https://druidv6.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?lastHongbaoId=0&pn=1&pz=20&type=2'
    # url = 'https://druidv6.if.qidian.com/Atom.axd/Api/HongBao/GetDetail?pn=1&pz=20&hongbaoId=1014574068370636800'
    # url = 'https://druidv6.if.qidian.com/Atom.axd/Api/HongBao/GetDetail?pn=1&pz=20&hongbaoId=1014579734875471872'
    print(header)

    response = requests.get(url=url, data={}, headers=header, verify=False)
    jsonData = json.loads(response.text)
    print()
    print(jsonData)
    with open('log/test.json', 'w', encoding='utf-8') as f:
        f.write(str(jsonData))