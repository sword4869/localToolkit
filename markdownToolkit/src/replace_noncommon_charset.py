
'''
替换字符 ０, \xef\xbc\x90 为 0



---

```python
# 字节编码
ch = b'\xef\xbc\xa0'
print(ch)

# 字节编码转utf-8字符串
print(ch.decode())

# utf-8字符串转字节编码
input_str = '１'
print(input_str.encode())
```
'''


input_path = 'source.txt'
output_path = 'destination.txt'

# 打印效果，对应正常字符，字节编码
charset = [
    [' ', ''],
    ['０', '0', '\xef\xbc\x90'],
    ['１', '1', '\xef\xbc\x91'],
    ['２', '2', '\xef\xbc\x92'],
    ['３', '3', '\xef\xbc\x93'],
    ['４', '4', '\xef\xbc\x94'],
    ['５', '5', '\xef\xbc\x95'],
    ['６', '6', '\xef\xbc\x96'],
    ['７', '7', '\xef\xbc\x97'],
    ['８', '8', '\xef\xbc\x98'],
    ['９', '9', '\xef\xbc\x99'],
    ['Ａ', 'A', '\xef\xbc\xa1'],
    ['Ｂ', 'B', '\xef\xbc\xa2'],
    ['Ｃ', 'C', '\xef\xbc\xa3'],
    ['Ｄ', 'D', '\xef\xbc\xa4'],
    ['Ｅ', 'E', '\xef\xbc\xa5'],
    ['Ｆ', 'F', '\xef\xbc\xa6'],
    ['Ｇ', 'G', '\xef\xbc\xa7'],
    ['Ｈ', 'H', '\xef\xbc\xa8'],
    ['Ｉ', 'I', '\xef\xbc\xa9'],
    ['Ｊ', 'J', '\xef\xbc\xaa'],
    ['Ｋ', 'K', '\xef\xbc\xab'],
    ['Ｌ', 'L', '\xef\xbc\xac'],
    ['Ｍ', 'M', '\xef\xbc\xad'],
    ['Ｎ', 'N', '\xef\xbc\xae'],
    ['Ｏ', 'O', '\xef\xbc\xaf'],
    ['Ｐ', 'P', '\xef\xbc\xb0'],
    ['Ｑ', 'Q', '\xef\xbc\xb1'],
    ['Ｒ', 'R', '\xef\xbc\xb2'],
    ['Ｓ', 'S', '\xef\xbc\xb3'],
    ['Ｔ', 'T', '\xef\xbc\xb4'],
    ['Ｕ', 'U', '\xef\xbc\xb5'],
    ['Ｖ', 'V', '\xef\xbc\xb6'],
    ['Ｗ', 'W', '\xef\xbc\xb7'],
    ['Ｘ', 'X', '\xef\xbc\xb8'],
    ['Ｙ', 'Y', '\xef\xbc\xb9'],
    ['Ｚ', 'Z', '\xef\xbc\xba'],
]











result = []
with open(input_path, 'r', encoding="utf-8") as fp:
    # 各行
    for line in fp.readlines():
        print(line)
        # 行中各字符
        for i in range(0, len(line)-1):
            # 各charset
            for j in range(len(charset)):
                line = line.replace(charset[j][0], charset[j][1])
                line = line.replace(charset[j][2], charset[j][1])
        result.append(line)

# 写入数据之writelines(s) : 每个列表元素拼接起来，不默认换行
with open(output_path, 'w', encoding="utf-8") as fp2:
    fp2.writelines(result)