from itertools import count
import requests

fileOldName = r'Usage\wifi-crack\readme.md'
fileNewName = r'Usage\wifi-crack\readme2.md'

imageDirSave = r'img'
imageDirMarkdown = r'https://github.com/sword4869/learn_netsecurity/blob/main/'+imageDirSave
imageCount = 0


# ---------------------------------------------------------------------



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
