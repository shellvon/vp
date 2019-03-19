简单的视频后台

利用豆瓣API提供搜索建议

利用最大资源采集视频信息

# API

#### 搜索建议
```bash
curl -X GET /api/suggest?q=X战警 


[{"episode":"","img":"https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2181156848.webp","title":"X战警：逆转未来","url":"https:\/\/movie.douban.com\/subject\/10485647\/?suggest=X%E6%88%98%E8%AD%A6","type":"movie","year":"2014","sub_title":"X-Men: Days of Future Past","id":"10485647"},{"episode":"","img":"https://img3.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2352321614.webp","title":"X战警：天启","url":"https:\/\/movie.douban.com\/subject\/25786060\/?suggest=X%E6%88%98%E8%AD%A6","type":"movie","year":"2016","sub_title":"X-Men: Apocalypse","id":"25786060"},{"episode":"","img":"https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p956878707.webp","title":"X战警：第一战","url":"https:\/\/movie.douban.com\/subject\/3168089\/?suggest=X%E6%88%98%E8%AD%A6","type":"movie","year":"2011","sub_title":"X-Men: First Class","id":"3168089"},{"episode":"","img":"https://img3.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2535222651.webp","title":"X战警：黑凤凰","url":"https:\/\/movie.douban.com\/subject\/26667010\/?suggest=X%E6%88%98%E8%AD%A6","type":"movie","year":"2019","sub_title":"X-Men: Dark Phoenix","id":"26667010"},{"episode":"","img":"https://img3.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2446530060.webp","title":"X战警","url":"https:\/\/movie.douban.com\/subject\/1295250\/?suggest=X%E6%88%98%E8%AD%A6","type":"movie","year":"2000","sub_title":"X-Men","id":"1295250"},{"episode":"","img":"https://img3.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2230029851.webp","title":"X战警3：背水一战","url":"https:\/\/movie.douban.com\/subject\/1401524\/?suggest=X%E6%88%98%E8%AD%A6","type":"movie","year":"2006","sub_title":"X-Men: The Last Stand","id":"1401524"}]

```

#### 视频搜索
```bash
curl -X GET /api/search?keyword=X战警
[{
    "actors": "休·杰克曼,詹姆斯·麦卡沃伊,迈克尔·法斯宾德,詹妮弗·劳伦斯", 
    "categories": "科幻片 ", 
    "cover": "http://tupian.tupianzy.com/pic/upload/vod/2018-04-23/201804231524450359.jpg", 
    "directors": "布莱恩·辛格", 
    "download_link": [
      {
        "name": "BD1280高清中英双字版", 
        "url": "http://xunleib.zuida360.com/1804/X战警：逆转未来.BD1280高清特效中英双字版.mp4"
      }
    ], 
    "id": "zuidazy_47834", 
    "language": "英语", 
    "name": "X战警：逆转未来", 
    "name_alias": "变种特攻：未来同盟战,X战警：未来昔日,X战警前传2：未来过去的日子,X战警前传2：未来昔日", 
    "note": "BD1280高清中英双字版", 
    "play_flash": [
      {
        "name": "BD1280高清中英双字版", 
        "url": "http://sohu.zuida-163sina.com/share/ZrCpiXLI3q2eqjUc"
      }
    ], 
    "play_m3u8": [
      {
        "name": "BD1280高清中英双字版", 
        "url": "http://sohu.zuida-163sina.com/20180423/qOaU44PY/index.m3u8"
      }
    ], 
    "poster": null, 
    "region": "美国", 
    "score": "8.2", 
    "source": "http://www.zuidazy.net/", 
    "synopsis": "故事的设定发生在当下，变种人族群遭到了前所未有的毁灭性打击，而这一切的根源是“魔形女”瑞文（詹妮弗·劳伦斯 Jennifer Lawrence 饰）在1973年刺杀了玻利瓦尔·特拉斯克（彼特·丁拉基 Peter Dinklage 饰）。在得知“幻影猫”（艾伦·佩吉 E llen Page 饰）利用穿越时空的能力帮助Blink（范冰冰 饰）等战友逃脱巨型机器人“哨兵”的追杀后，X教授（帕特里克·斯图尔特 Patrick Stewart 饰）和万磁王（伊恩·麦克莱恩 Ian McKellen 饰）达成认同，决定让金刚狼（休·杰克曼 Hugh Jackman 饰）穿越回1973年，找到年轻的X教授（詹姆斯·麦卡沃伊 James McAvoy 饰）和年轻的万磁王（迈克尔·法斯宾德 Michael Fassbender 饰）并说服他们一起阻止魔形女的行动。于是，金刚狼踏上了回到过去的旅程，但是命运会不会发生逆转，任何人都无从知晓。", 
    "url": "http://sohu.zuida-163sina.com/share/ZrCpiXLI3q2eqjUc", 
    "year": "2014"
  }
]
```

#### 视频详情

```bash
curl -X GET /api/movie/:source/:id
{
  "id": 123,
  "language": "Zh",
  // ...
}
```

#### 热门搜索
language

curl -X GET /api/movie/hot-search
[
  {
    "name": "xxx"
  },
  //...
]
