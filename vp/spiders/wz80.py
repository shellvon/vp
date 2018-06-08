# -*- coding: utf-8 -*-

import scrapy

from misc.spider import CommonSpider
from vp.items import FilmItem


class Wz80Spider(CommonSpider):
    name = 'wz80'
    start_urls = ['http://www.wz80.com/type/1.html']
    all_xpath_rules = {
        'data_list': '//div[@class="movie-item"]/a/@href',
        'next_page': '//a[contains(text(), "下一页")]/@href',
        'play_link': '//div[@class="movievod"]/ul/li/text()',
        'm3u8_link': None,
        'cover_img': '//img[@class="img-thumbnail"]/@src',
        'synopsis_text': '//p[@class="summary"]/text()',
        'video_details': '//div[@class="videoDetail"]/li[@class="sa"]|//div[@class="videoDetail"]/li[not(@class)]/div'
    }

    def parse_film_detail(self, response):
        seletor = response.selector
        name = seletor.xpath('//h1[@class="movie-title"]/text()').extract_first()
        cover = seletor.xpath(self.all_xpath_rules['cover_img']).extract_first()
        year = seletor.xpath('//span[@class="movie-year"]').re_first('(\d+)')
        synopsis = seletor.xpath(self.all_xpath_rules['synopsis_text']).extract_first()
        film_details = seletor.xpath('//table/tbody/tr/td[2]/text()').extract()

        film = FilmItem(
            source=self.name,
            name=name,
            year=year,
            category=film_details[2].replace('/', ','),  # 分类
            region=film_details[3],
            cover=cover,
            director=film_details[0].replace('/', ','),
            actors=film_details[1].replace('/', ','),
            synopsis=synopsis,
            language=film_details[4].replace('/', ',')
        )
        url = seletor.xpath('//li[@class="dslist-group-item"]/a/@href').extract_first()
        yield response.follow(url, meta={'film': film}, callback=self.parse_film_m3u8)

    def parse_film_m3u8(self, response):
        film = response.meta['film']
        url = response.selector.xpath('//iframe/@src').extract_first()  # not m3u8
        if url:
            film['url'] = url
        return film
