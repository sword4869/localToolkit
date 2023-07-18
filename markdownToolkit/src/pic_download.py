'''
将csdn在线的markdown图片路径，下载下来保存到本地。
1. 在 `markdownToolkit/image` 下创建 `source.md`。复制上在线版本的markdown
2. python pic_download.py -r

将本地markdown图片迁移
1. 不用创建source.md, 直接 python pic_download.py -l -t D:\git\test\aa

'''


import os
import time
import configargparse
import requests
import shutil 
import random
##################    CONFIGURATION START    ##################
input_path = os.path.abspath(os.path.join('../image/source.md'))
output_path = os.path.abspath(os.path.join('../image/destination.md'))
imageNameSavePath = os.path.abspath(os.path.join('../image'))
# 在markdown的`![]()`中文档相对于image的路径
imageNameMarkdownPath = '.'
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
# 返回在markdown中图片路径：`![xxx](xxx)`
def downloadImage(url, imageNameSave):
    # print(f'\033[4m[url[{url}] is dealing...\033[m')

    # 下载一个图片
    response = requests.get(url)

    # 写入图片
    with open(imageNameSave, 'wb') as fp:
        # 判断状态码
        if response .status_code == 404:
            print(f'{response.status_code}.status_code ={url}')
            return None
        # 写入数据
        else:
            fp.write(response.content)
            return newLine

def mvLocalImage(url, imageNameSave):
    shutil.move(url, imageNameSave)
    pass

if __name__ == '__main__':

    parser = configargparse.ArgumentParser()

    parser.add_argument('-r', '--remote', action='store_true', help='download the images of remote markdown images')
    parser.add_argument('-l', '--local', action='store_true', help='mv the images of local markdown images')
    parser.add_argument('-t', '--target_source', type=str, help='the working path of the local markdown file')
    args = parser.parse_args()

    if args.local:
        shutil.copy(args.target_source, input_path)

    lines = []
    with open(input_path, 'r', encoding="utf-8") as fp:
        # 各行
        for line in fp:
            # 从一行中提取图片的url
            url = getUrl(line)
            # 没有，就原封不动
            if(url == None):
                lines.append(line)
                continue
                
            # 如果有，则下载，并修改成本地图片的格式
            print(f'>>> {line}')
            
            postfix = url.rfind('.')
            time_stamp = str(time.time()).replace('.', '')
            time_stamp += str(random.randint(1000, 9999))
            imageName = f'{time_stamp}{url[postfix:]}'
            # 在markdown的`![]()`中文档相对于image的路径
            imageNameMarkdownPath_all = imageNameMarkdownPath + '/' + imageName
            newLine = f'![{imageName}]({imageNameMarkdownPath_all})\n'
            print(f'<<< {newLine}')

            # 下载的图片放在image文件夹
            imageNameSave = imageNameSavePath + '/' + imageName

            if args.remote:
                if downloadImage(url, imageNameSave):
                    lines.append(newLine)
                else:
                    raise Exception('404:', line)
            elif args.local:
                url = os.path.join(args.target_source, '..', url)
                mvLocalImage(url, imageNameSave)
                lines.append(newLine)
            else:
                raise Exception('please enter the args `local` or `remote`')
                
    # 写入数据之writelines(s) : 每个列表元素拼接起来，不默认换行
    with open(output_path, 'w', encoding="utf-8") as fp2:
        fp2.writelines(lines)
