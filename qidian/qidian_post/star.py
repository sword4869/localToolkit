import json

lines = [
    '[DEFAULT]\n',
    'url_base : https://h5.if.qidian.com/argus/api/v1/circle/post/getshare?\n'
]

with open(r"listpostcollection.json", 'r', encoding='utf-8') as fp:
    text = fp.readline()
    jsonData = json.loads(text)
    totalCount = int(jsonData['Data']['TotalCount'])
    for i in range(0,totalCount):
        content = jsonData['Data']['TopicDataList'][i]
        # 圈子
        circleId = content['CircleId']
        # 帖子
        postId = content['Id']
        # 回复数
        totalCountHistory = content['PostCount']
        # 运营官
        NickName = content['TitleInfoList'][0]['NickName']
        # 日期
        date = content['Subject'][6:8]
        line = '[{}]\ncircleId={}\npostId={}\ntotalCountHistory={}\nNickName={}\ndate={}\n'.format(i, circleId, postId, totalCountHistory, NickName, date)
        lines.append(line)

with open(r"demo3.ini", 'w', encoding='utf-8') as fp:
    fp.writelines(lines)