from fake_useragent import UserAgent
import requests

url = input('url:')

save_path = input('save_path(file_name):')
# print('[save_path]', save_path)

try:
    headers = {'User-Agent': UserAgent(verify_ssl=False).random}
    response_file = requests.get(url=url, headers=headers)

    # 判断状态码
    if response_file.status_code == 200:
        with open(save_path, 'wb') as fp:
            fp.write(response_file.content)
    else:
        print(url, '404')
        pass
except Exception as e:
    print(url, e)
    pass
