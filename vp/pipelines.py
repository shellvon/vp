# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class FilmPipeline(object):

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, None)
        if not item['url']:
            raise DropItem('【{name}】[{source}]缺少播放链接'.format(**item))

        def to_arr(x, sep):
            return list(map(lambda el: el.strip(), x.split(sep)))

        category = item['category']
        if category:
            item['category'] = to_arr(category, ',')
        actors = item['actors']
        if actors:
            item['actors'] = to_arr(actors, ',')
        directors = item['director']
        if directors:
            item['director'] = to_arr(directors, ',')
        year = item['year']
        if year == '未知':
            item['year'] = None
        return item
