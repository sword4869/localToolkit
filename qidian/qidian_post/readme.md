- [Purpose](#purpose)
- [Use Step](#use-step)
# Purpose

To know which post about Month Ticket Activity is locked in the app of qidianReader.

# Use Step

> star the post

We star many posts( Find ->  Red envelopes square -> Activity), which is convinent to deal with automatically.

> HttpCanary

HttpCanary is an app in Android which is used for catching web package. It is like browser's developer tool.

So after you start HttpCanary and set target app (qidianReader), we start qidianReader (Me -> Star -> Posts).

Now, the package is catched. We get into HttpCanary, look for the url

```http
https://druidv6.if.qidian.com/argus/api/v1/circle/listpostcollection?pg=1&pz=20
```

And save its json response. This file is `listpostcollection.json`.

> abstract the json

we use `star.py` to abstract `listpostcollection.json` and save the result in `demo3.ini`.

The following is what we abstract:

```http
[0]
circleId=21395400108453704
postId=769496312734351360
totalCountHistory=0
NickName=夏天★
date=29
```

- `circleId` and `postId` is used for ensure a certain post.
- `totalCountHistory` is the count of post's comment. Beacause we cannot directly get the post's lock value(need to hack QRsign and so on, which is the security system in app), we determine the locking situation by judging the increase of comments after the post is opened.
- `NickName` is the nickname of Book Manager. It is a message for print result.
- `date` is a trick that if today is 29 and the post will be opened in 30, we can hop it.

> demo3.py

We read information of `demo3.ini`, compose the url of each post, judge the lock situation. If post is opend, the program will notify us by local computer BingBing sound and remote pushplus wechat message.

And log the program running time in `log.txt`. The `[2, 3, 5]` means the sections of the posts open today and before.

Tricks:

- fake User-Agent. `fake_useragent`
- ini configuration. `configparser`
- notification. `winsound` and `http://www.pushplus.plus`.
