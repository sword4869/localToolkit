
input_path = 'source.txt'
output_path = 'destination.txt'

result = []
with open(input_path, 'r', encoding="utf-8") as fp:
    # 各行
    for line in fp.readlines():
        print(line)
        # 行中各字符
        for i in range(0, len(line)-1):
            
        result.append(line)

# 写入数据之writelines(s) : 每个列表元素拼接起来，不默认换行
with open(output_path, 'w', encoding="utf-8") as fp2:
    fp2.writelines(result)