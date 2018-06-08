# -*- coding: utf-8 -*-
from misc.spider import CommonSpider

from vp.items import FilmItem


class Zy131Spider(CommonSpider):
    """
    以下站点一样:
        http://www.131zyw.com/?m=vod-type-id-1.html
        http://zy135.com/?m=vod-type-id-1.html
    """

    name = 'zy131'

    start_urls = ['http://www.131zyw.com/?m=vod-type-id-1.html']

    keys_map = {
        '别名: ': 'name_alias',
        '备注: ': 'note',
        '主演: ': 'actors',
        '导演: ': 'director',
        '类型: ': 'category',
        '语言: ': 'language',
        '地区: ': 'region',
        '上映: ': 'year',
    }

    all_xpath_rules = {
        'data_list': '//span[@class="xing_vb4"]/a/@href',
        'next_page': '//a[contains(text(), "下一页")]/@href',
        'play_link': '//div[@class="vodplayinfo"]/div/ul/li/text()',
        'm3u8_link': '//div[@class="vodplayinfo"]/div/ul/li[contains(text(), ".m3u8")]',
        'cover_img': '//div[@class="vodImg"]/img/@src',
        'synopsis_text': '(//div[@class="vodplayinfo"])[2]/text()',
        'video_details': '//div[@class="vodinfobox"]/ul/li[not(@class)]'
    }

    def parse_film_detail(self, response):
        film = FilmItem(source=self.name)
        name, note, score = response.selector.xpath('//div[@class="vodh"]/*/text()').extract()
        film['name'] = name  # 电影名
        film['note'] = note  # 电影备注.

        response.meta['film'] = film
        return super(Zy131Spider, self).parse_film_detail(response)
