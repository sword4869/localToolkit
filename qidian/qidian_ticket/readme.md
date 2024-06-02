- [adbswipe, just\_swipe](#adbswipe-just_swipe)
- [make\_borgus](#make_borgus)
- [make\_headers](#make_headers)
- [🚀onestand\_post](#onestand_post)
- [解析](#解析)
  - [月票和推荐票](#月票和推荐票)
  - [headers](#headers)

---

# adbswipe, just_swipe

实时adb滑动刷新，识图和自动点击投票。

技术栈：
- 用adb来swipe刷新、点击投票。
- 用opencv基于截图的颜色来判断是否有票。

`pos.yaml` 是配置信息。关键坐标、颜色等信息。

# make_borgus

批量设置手机时钟，刷新出一波抓包信息。

```bash
# 提前进入shell，然后点击窗口，让pyguiauto自动输入
PS C:\Users\lab> adb shell
RMX2205CN:/ $ su
```

然后，我们再进入小黄鸟，分享网易邮箱给自己。

# make_headers

调试用的，将邮箱里的东西都保存到 `log/test` 下。

# 🚀onestand_post

小黄鸟捕获请求和响应，共享给邮箱发送给自己。

读取邮箱，去掉GET描述信息第一行，写入到yml中。还会根据GET头还分类月票还是推荐票。

GetHeaders根据yml来补全header。

Poster加载header，发送请求，获取到红包信息的json文件。

# 解析

## 月票和推荐票

月票的api是`https://druidv6.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?lastHongbaoId=0&pn=1&pz=20&type=1`

推荐票的api是`https://druidv6.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?lastHongbaoId=0&pn=1&pz=20&type=2`

区别是type

既然是不同api，那么headers信息也需要不同。也就是说，我们需要分别刷新和抓包。

## headers
```json
{
    'borgus': ...,
    'tstamp': ...,
    'User-Agent': 'Mozilla/mobile QDReaderAndroid',
    'Cookie': 'QDInfo=6JopQVMlApWCQKIyEIM/sqWTTghkgQgMl3NDGmeZtr6I75X1QN0BYrGDF2Vtwl36vldl0NxNjvGyHJ9evuJteBV3v+i2FcrCEFH7gIbBuE4+yyFxnwYlRMjguKijIK6xW2SJJ/jU+byLV3a71hfMxQkyrjoJE1bZgu2UR/E7WMXALROy/H2vt1Yqcd+PB4zs2Fjb6TK9jVhD5/6KtcopGWUv5nUcLOsU+IZuwZibxv2YrCD/CLPAl3YUg8bHRLy1KjyW6Otajo4LUWxZedF6lQHAzxGU5B38NdWtcQ6HDdgOgeq2YXr2ZlNG6BT7bKX81S845+Sh2fjEO6fmNGVvefUPylkSgXkbfg1OoU+yPChdMDMyUNuCKQ==',
    'Host': 'druidv6.if.qidian.com'
}
```
borgus和tstamp十五分钟一次，比如`'2023-01-30 09:40:00', 1675042800`。这个可以在手机上修改日期，app会提示时钟不符合。

`User-Agent`中` Mozilla/mobile QDReaderAndroid/7.9.266/860/1000015`，无须具体版本。

- 2024/06月前

    `Cookie`中只有QDInfo是必要的，而且这个QDInfo不会过期。

    ```python
    'Cookie': 'QDInfo=6JopQVMlApWCQKIyEIM/sqWTTghkgQgMl3NDGmeZtr6I75X1QN0BYrGDF2Vtwl36vldl0NxNjvGyHJ9evuJteBV3v+i2FcrCEFH7gIbBuE4+yyFxnwYlRMjguKijIK6xW2SJJ/jU+byLV3a71hfMxQkyrjoJE1bZgu2UR/E7WMXALROy/H2vt1Yqcd+PB4zs2Fjb6TK9jVhD5/6KtcopGWUv5nUcLOsU+IZuwZibxv2YrCD/CLPAl3YUg8bHRLy1KjyW6Otajo4LUWxZedF6lQHAzxGU5B38NdWtcQ6HDdgOgeq2YXr2ZlNG6BT7bKX81S845+Sh2fjEO6fmNGVvefUPylkSgXkbfg1OoU+yPChdMDMyUNuCKQ==',
    ```
- 2024/06月
    
    ywkey, cmfuToken, QDInfo是必须的，否则报错。但这基本全乎了，那就直接cookie算了。
    ```python
    'Cookie': 'ywkey=ywNNnDI6o8sg; cmfuToken=N((SD9JrKbwX28eGq14hAZGB6RIJBkPHwZ1116owWhxacq7t_VMzprlGKKgTA3AutPb6PE_jsODvxrbM2SQeviNzTL_xGgDTMzTC_97_Js20Qv0e-E1jK-zf4dVVxHt2JwfL4o2aKyi77sH_7nLCB6fKKF386OrfcaNlDfXAwuYL4btGiSjxsE1JgQJFmRrOQL_efN1oxhtfm95Lq46M2O8uEbSsf74g5B7Nep15LHK1uJjFCe8qxP5Y1jBCKnLIw8ypJrzkRUplO_hQQ7JRbZi1Q2; QDInfo=6JopQVMlApWCQKIyEIM/sqWTTghkgQgMl3NDGmeZtr6I75X1QN0BYhslB10qXhUuIa6hoCNR3vqH8D615NCmZQAKScxs81Mv8BR06X9t3nJo3sG5GsrsK2WKXGCZGItQLoDY0uBvJ8la8JUaLOPRijp02le8y5PkvtF5TaxdSQrPyzzJ5zrLqAUCPmTHNeCKNoSxuULRwVdxDPQFQILjGZd27qBDV05c6OkvSc/w9cbUVzE8uGMUO3AbgDb8vGN33HCQ66tFJcEjeXuUGy8f8BZjRz2g8+QQn5w9n5OwIA3Luz4NEuWRORnsXC1HOjZMVptQ8k879a3AkPxKMbOPvH/sL6+ERaUwfUdKVX2EPkUv7GMzD2QHNw==',
    ```

    而且月票和推荐票的cookie还不通用。