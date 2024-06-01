import requests
import urllib3
from fake_useragent import UserAgent

# for InsecureRequestWarning
urllib3.disable_warnings()

class Extractor:
    def extract(self,filePath):
        links = []
        with open(filePath, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            for line in lines:
                if line.startswith('https'):
                    # omit the last charater '\n'
                    line = line[0:-1]
                    links.append(line)
        return links

    def download(self, link, name):
        print(f"{name} is downloading...")
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(url=link, headers=headers, verify=False)
        
        if response.status_code != 200:
            raise Exception(f'{response.status_code} \n {response.content}')

        with open(name, 'wb') as fp:
            fp.write(response.content)
        return name

if __name__ == '__main__':
    filePath = 'm3u8.txt'
    extractor = Extractor()
    links = extractor.extract(filePath)
    print(links[0])
    name = extractor.download(links[0], '0.ts')
    print(name)