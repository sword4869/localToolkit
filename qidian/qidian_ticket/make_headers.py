from src.MyEmail import MyEmail

if __name__ == '__main__':
    type = 'yuepiao'
    type = 'tuijianpiao'
    myEmail = MyEmail()
    myEmail.build_connect()
    myEmail.activate()
    contents = myEmail.get_contents(filter=False)
    print("waiting for email...", len(contents) > 0)

    for i, content in enumerate(contents):
        with open(f'log/test/content_{i}.yml', 'wb') as f:
            f.write(content)
    
    # 过滤content中以'GET /Atom.axd' 开头的文件
    filtered_index = []
    for i in range(len(contents)):
        with open(f'log/test/content_{i}.yml', 'rb') as f:
            content = f.read()
            if content.startswith(b'GET /Atom.axd'):
                filtered_index.append(i)
    print(filtered_index)

    for i, fi in enumerate(filtered_index):
        with open(f'log/test/content_{fi}.yml', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = lines[1:]
            # tstamp
            tstamp = lines[3].split(': ')[1][:-1]
            # 转化tstamp为时间字符串
            from src.TimeTransformer import TimeTransformer
            tstamp_str = TimeTransformer().timestamp2str_time(int(tstamp//1000), '%H%M%S')
            
            with open(f'log/test/filtered_content_{tstamp}_{tstamp_str}.yml', 'w', encoding='utf-8') as f:
                f.writelines(lines)
            