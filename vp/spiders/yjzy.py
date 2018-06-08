# -*- coding: utf-8 -*-
from misc.spider import CommonSpider


class YjzySpider(CommonSpider):
    """
    永久资源采集
    """
    name = 'yjzy'
    start_urls = ['http://www.yongjiuzy.com/?m=vod-type-id-1.html']

    all_xpath_rules = {
        'data_list': '//tbody[@id="data_list"]/tr/td[1]/a/@href',
        'next_page': '//a[contains(text(), "下一页")]/@href',
        'play_link': '//div[@class="movievod"]/ul/li/text()',
        'm3u8_link': '//div[@class="movievod"]/ul/li[contains(text(), ".m3u8")]',
        'cover_img': '//div[@class="videoPic"]/img/@src',
        'synopsis_text': '//div[@class="movievod"]/p/text()',
        'video_details': '//div[@class="videoDetail"]/li[@class="sa"]|//div[@class="videoDetail"]/li[not(@class)]/div'
    }
