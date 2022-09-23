import chardet

input_str = b"\262\273\326\252\265\300\325\342\321\371\265\304\326\367\273\372\241\243"
byte_str_charset = chardet.detect(input_str)  # 获取字节码编码格式

output_str = str(input_str, byte_str_charset.get('encoding'))  # 将八进制字节流转化为字符串
print(byte_str_charset, output_str)