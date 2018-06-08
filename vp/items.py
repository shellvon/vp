# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FilmItem(scrapy.Item):
    source = scrapy.Field()  # 电影来源
    name = scrapy.Field()  # 电影名字
    name_alias = scrapy.Field()  # 电影别名
    note = scrapy.Field()  # 备注
    category = scrapy.Field()  # 电影类型
    region = scrapy.Field()  # 地区
    cover = scrapy.Field()  # 封面图
    poster = scrapy.Field()  # 播放时需用第一帧图.
    url = scrapy.Field()   # 播放地址
    actors = scrapy.Field()  # 领衔主演
    director = scrapy.Field()  # 导演
    synopsis = scrapy.Field()  # 简介
    language = scrapy.Field()  # 语言
    year = scrapy.Field()  # 上映年份
