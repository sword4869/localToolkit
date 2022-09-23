- [1. 获取参数sys](#1-获取参数sys)
  - [1.1. sys 模块](#11-sys-模块)
  - [1.2. 例子](#12-例子)
    - [1.2.1. 基本特性](#121-基本特性)
    - [1.2.2. 都是str类型](#122-都是str类型)
    - [1.2.3. xxx.py及其之后的才是](#123-xxxpy及其之后的才是)
    - [1.2.4. 空格和转移字符](#124-空格和转移字符)
- [2. 解析参数getopt](#2-解析参数getopt)
  - [2.1. getopt模块](#21-getopt模块)
    - [2.1.1. 思想](#211-思想)
    - [2.1.2. 函数](#212-函数)
  - [2.2. 例子](#22-例子)
    - [2.2.1. 简单](#221-简单)
    - [2.2.2. 提取元组](#222-提取元组)
---

# 1. 获取参数sys
这里我们**只需要获取控制台输入的字符串是啥，直接抄过来。**
## 1.1. sys 模块
```python
import sys
```
- 访问到所有的命令行参数：
	- `python xxx.py`中`xxx.py`**及其之后的才是**，之前的不是。
	- **要编译的`.py`文件就是第一个参数**。
- 它的返回值`sys.argv`：**列表(list)类型**
	- 参数个数： `len(sys.argv)`
	- 访问列表元素：`sys.argv[i]`。
		- **从0开始**，第一个`sys.argv[0]`就是`.py`文件。
		- **都是字符串类型。**
- 参数
	- 以空格分离
	- 可以被`''`包含着输入空格
	- 转移字符`\`传入后多带一个`\`

## 1.2. 例子
### 1.2.1. 基本特性
```python
import sys

print(sys.argv)
print(type(sys.argv))
print(sys.argv[0])
```
![1663935316.png](/image/1663935316.png)
### 1.2.2. 都是str类型
```python
import sys

print(sys.argv)
print(sys.argv[1])
print(type(sys.argv[1]))
```
![1663935317.png](/image/1663935317.png)
### 1.2.3. xxx.py及其之后的才是
```python
import sys

print(sys.argv)
```
![1663935317.png](/image/1663935317.png)
- 第一个`-u`不是，因为它是传给编译器的参数，只有xxx.py及其之后的才是
- 第二个`-u`是，可以看到被读取到了。

### 1.2.4. 空格和转移字符
```python
import sys

print(sys.argv)
```
![1663935318.png](/image/1663935318.png)
- 以空格分离
- 可以被`''`包含着输入空格
- 转移字符`\`传入后多带一个`\`

# 2. 解析参数getopt
在sys模块的基础上，我们不仅要获取命令行参数，还要将每个参数和对应的变量关联起来。

比如：输入用户名username和密码password
- 用sys是`python xxx.py 3 4`，我们还得自己还得保证`3`对应用户名username和`4`对应密码password。
- 而用getopt是`python xxx.py -u 3 -p 4`或`python xxx.py -p 4 -u 3`，这样就不怕对应不上了。
## 2.1. getopt模块
```python
# 需要用sys.argv[1:]参数
import sys
import getopt
```
### 2.1.1. 思想
getopt怎么解析参数的？

- 我们知道`-u`和`3`对应、`-p`和`4`对应，这种形式很像键值对，那么我们就可以**用一个元组将其分别存储起来**，然后**将这些元组整合在一起成为一个列表**。
- 同时，有的命令参数**不需要对应的值**，比如常见的`-h`表示需要帮助。我们**也用元组储存，对应的值为空就行**。
- 解析键值对的时候，是顺序解析的，碰到解析错误时后面就不解析全归入错误的第二个返回值args中了。比如要`-h -u 3 -p 4`，却输入错误的`-h 3 -u -p 4`。
![1663935318.png](/image/1663935318.png)

### 2.1.2. 函数
原型：
```python
getopt.getopt(args, options[, long_options])
```
例子：
```python
opts, args = getopt.getopt(sys.argv[1:], "hu:p:",
                               ["help", "username=", "password="])
# 三种参数,help(h),username(u),password(p)。第一个不需要值，另外两个需要值
```
- args：表示要解析的命令行参数，为`sys.argv[1:]`。
因为要解析的是键值对的参数，而`sys.argv[0]`表示文件`xxx.py`，不对应键值对。
**注意：当传入文件名(即`sys.argv`)是会解析错误的，你会发现后面的参数匹配不上。**
- options：`-u`这种带个`-`的形式，表示短格式分析串。
	- 用字符串`""`
	- 一个字母即表示一种参数（键值对的键）
	- 字母后跟`:`表示需要值，不跟表示不需要值。
- long_options：`--usename`这种带个`--`的形式，表示长格式分析串。
	- 用列表`[]`
	- 一个单词即表示一种参数（键值对的键）
	- 单词后跟`=`表示需要值，不跟表示不需要值。
- 返回值：
	- 第一个返回的是**元组的列表**，表示成功对应的参数
	- 第二个返回的是**列表**，表示对应失败无法解析的参数
## 2.2. 例子
### 2.2.1. 简单
```python
# 需要用sys.argv[1:]参数
import sys
import getopt

print(sys.argv)

try:
	# 三种参数,help(h),username(u),password(p)。第一个不需要值，另外两个需要值
    opts, args = getopt.getopt(sys.argv[1:], "hu:p:",
                               ["help", "username=", "password="])
	# 元组的列表，表示成功对应的参数
    print('[opts]', opts)
    # 列表，表示对应失败无法解析的参数
    print('[args]', args)
# 报错是getopt.GetoptError
except getopt.GetoptError:
    print('[getopt.GetoptError]')
    sys.exit()
```

输入的时候：
- 短：`-u 3`或`-u3`
- 长：`--username 3`或`--username=3`

### 2.2.2. 提取元组
就是处理每个元组
```python
import sys
import getopt

print(sys.argv)

try:
    opts, args = getopt.getopt(sys.argv[1:], "hu:p:",
                               ["help", "username=", "password="])

    username = ""
    password = ""
    # 就是处理每个元组
    for k, v in opts:
        if k in ("-h", "--help"):
            print('[-h --help]')
        elif k in ("-u", "--username"):
            username = v
            print('[-u --username]', username)
        elif k in ("-p", "--password"):
            password = v
            print('[-p --password]', password)
    print('[username]', username)
    print('[password]', password)
except getopt.GetoptError:
    print('[getopt.GetoptError]')
    sys.exit()
```
![1663935318.png](/image/1663935318.png)
