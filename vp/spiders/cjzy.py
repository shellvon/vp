# -*- coding: utf-8 -*-

from misc.spider import CommonSpider


class CjzySpider(CommonSpider):
    name = 'cjzy'
    start_urls = ['http://www.caijizy.com/?m=vod-type-id-1.html']
