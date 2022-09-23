'''
【效果】
不换行

【例子】
原文：
1
2
3

输出：
123
'''

input_path = 'source.txt'
output_path = 'destination.txt'

result = []


with open(input_path, 'r', encoding="utf-8") as fp:
    # 各行
    for line in fp.readlines():
        print(line)
        result.append(line[0:-1])

# 写入数据之writelines(s) : 每个列表元素拼接起来，不默认换行
with open(output_path, 'w', encoding="utf-8") as fp2:
    fp2.writelines(result)
