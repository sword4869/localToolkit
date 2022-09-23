import requests

input_path = 'source.txt'
output_path = 'destination.txt'

def getUrl(line):
    length = len(line)
    # `![]()`最低要求
    if(length < 5):
        return 0
    # 前缀
    if(line.startswith('![') == False):
        return 0
    # 查括号
    l_bracket = line.find('(')
    r_bracket = line.find(')')
    # 找到了url还不够,`https://xxxx.jpg?size=960`，可能会有这样的修饰，比如csdn。
    content = line[l_bracket + 1:r_bracket]

    # 截取到图片后缀格式
    postfixList = ['.png', '.jpg']
    for i in postfixList:
        postfix = content.find(i)
        # 找到了
        if postfix != -1:
            return content[0:postfix] + i

    return 0
    pass


def downloadImage(url):
    print('url[{0}] is dealing.'.format(url))

    # 下载一个图片
    response = requests.get(url)
    global imageCount
    postfix = url.rfind('.')
    imageName = str(imageCount) + url[postfix:]
    imageNameSave = imageDirSave + '/' + imageName
    imageNameMarkdown = imageDirMarkdown + '/' + imageName

    # 写入图片
    with open(imageNameSave, 'wb') as fp:
        # 判断状态码
        if response .status_code == 404:
            print(['response.status_code'], response.status_code, url)
            return 0
        # 写入数据
        else:
            fp.write(response.content)
            imageCount += 1

            newLine = '![{0}]({1})\n'.format(imageName, imageNameMarkdown)
            return newLine
    pass


lines = []
with open(input_path, 'r', encoding="utf-8") as fp:
    # 各行
    for line in fp:
        # 从一行中提取图片的url
        url = getUrl(line)
        print(line)
        # 如果有，则下载，并修改成本地图片的格式
        if(url != 0):
            newLine = downloadImage(url)
            if(newLine != 0):
                lines.append(newLine)
        # 没有，就原封不动
        else:
            lines.append(line)

# 写入数据之writelines(s) : 每个列表元素拼接起来，不默认换行
with open(output_path, 'w', encoding="utf-8") as fp2:
    fp2.writelines(lines)