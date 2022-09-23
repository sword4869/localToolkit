from itertools import count
import requests

fileOldName = r'Usage\wifi-crack\readme.md'
fileNewName = r'Usage\wifi-crack\readme2.md'

imageDirSave = r'img'
imageDirMarkdown = r'https://github.com/sword4869/learn_netsecurity/blob/main/'+imageDirSave
imageCount = 0


# ---------------------------------------------------------------------

def getUrl(line):
    length = len(line)
    if(length < 5):
        return 0
    if(line.startswith('![') == False):
        return 0
    l_bracket = line.find('(')
    r_bracket = line.find(')')
    content = line[l_bracket + 1:r_bracket]

    postfixList = ['.png', '.jpg']
    for i in postfixList:
        postfix = content.find(i)
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
# 同时读写之r+ : 写后就不能读出(读出空字符串)
with open(fileOldName, 'r', encoding="utf-8") as fp:
    for line in fp:
        # print(line)
        url = getUrl(line)
        if(url != 0):
            newLine = downloadImage(url)
            if(newLine != 0):
                lines.append(newLine)
        else:
            lines.append(line)

with open(fileNewName, 'w', encoding="utf-8") as fp2:
    fp2.writelines(lines)
