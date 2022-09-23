import requests
import time


##################    CONFIGURATION START    ##################
input_path = '../source.txt'
output_path = '../destination.txt'
relativePath = '/image'

###################    CONFIGURATION END    ###################

# 从一行中提取图片的url
# 成功则返回图片连接，失败则返回None
def getUrl(line):
    length = len(line)
    # `![]()`最低要求
    if(length < 5):
        return None
    # 前缀
    if(line.startswith('![') == False):
        return None
    # 查括号
    l_bracket = line.find('(')
    r_bracket = line.find(')')
    # 找到了url还不够,`
    # 第一，不算图片格式。`https://xxx.md`
    # 第二，修饰问题。`https://xxxx.jpg?size=960`，可能会有这样的修饰，比如csdn。
    content = line[l_bracket + 1:r_bracket]

    # 截取到图片后缀格式
    postfixList = ['.png', '.jpg']
    for i in postfixList:
        postfix = content.find(i)
        # 找到了
        if postfix != -1:
            return content[0:postfix] + i

    # 后缀格式不匹配
    return None
    pass

# 下载图片，并存储在image文件夹下
def downloadImage(url):
    # print(f'\033[4m[url[{url}] is dealing...\033[m')

    # 下载一个图片
    response = requests.get(url)
    postfix = url.rfind('.')
    time_stamp = int(time.time())
    imageName = f'{time_stamp}{url[postfix:]}'
    # 下载的图片放在image文件夹
    imageNameSave = '../image' + '/' + imageName
    # 在markdown的`![]()`中文档相对于image的路径
    imageNameMarkdown = relativePath + '/' + imageName

    # 写入图片
    with open(imageNameSave, 'wb') as fp:
        # 判断状态码
        if response .status_code == 404:
            print(f'{response.status_code}.status_code ={url}')
            return None
        # 写入数据
        else:
            fp.write(response.content)
            newLine = f'![{imageName}]({imageNameMarkdown})\n'
            return newLine
    pass


lines = []
with open(input_path, 'r', encoding="utf-8") as fp:
    # 各行
    for line in fp:
        # 从一行中提取图片的url
        url = getUrl(line)
        # 如果有，则下载，并修改成本地图片的格式
        if(url != None):
            print(f'\033[44m{line}\033[m')
            newLine = downloadImage(url)
            if(newLine != None):
                lines.append(newLine)
                print(f'\033[45m{newLine}\033[m')
            else:
                raise Exception('404:', line)
        # 没有，就原封不动
        else:
            lines.append(line)

# 写入数据之writelines(s) : 每个列表元素拼接起来，不默认换行
with open(output_path, 'w', encoding="utf-8") as fp2:
    fp2.writelines(lines)
