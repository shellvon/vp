# -*- coding: utf-8 -*-
from urllib.parse import urlparse, parse_qs

import scrapy

from vp.items import FilmItem


class CommonSpider(scrapy.Spider):
    keys_map = {
        '影片名称: ': 'name',
        '影片别名: ': 'name_alias',
        '影片备注: ': 'note',
        '影片主演: ': 'actors',
        '影片导演: ': 'director',
        '栏目分类: ': 'category',
        '语言分类: ': 'language',
        '影片地区: ': 'region',
        '上映年份: ': 'year',
    }

    all_xpath_rules = {
        'data_list': '//tbody[@id="data_list"]/tr/td[1]/a/@href',
        'next_page': '//a[contains(text(), "下一页")]/@href',
        'play_link': '//div[@class="movievod"]/ul/li/text()',
        'm3u8_link': '//div[@class="movievod"]/ul/li[contains(text(), ".m3u8")]',
        'cover_img': '//div[@class="videoPic"]/img/@src',
        'synopsis_text': '//div[@class="movievod"]/p/text()',
        'video_details': '//div[@class="videoDetail"]/li[@class="sa"]|//div[@class="videoDetail"]/li[not(@class)]/div'
    }

    m3u8_path_regexs = [
        'var main = "([^"]+)"',  # https://videos2.jsyunbf.com/share/goIhGy3xA1hoPfMe
        'var huiid = "([^"]+)"',
    ]

    def parse_film_detail(self, response):
        film = response.meta.get('film', FilmItem(source=self.name))
        img_src = response.selector.xpath(self.all_xpath_rules['cover_img']).extract_first()
        # film_cover = parse_qs(urlparse(img_src).query)['url'][0]
        film['cover'] = img_src
        for sel in response.selector.xpath(self.all_xpath_rules['video_details']):
            txt = sel.xpath('text()').extract()
            if len(txt) != 2:
                continue
            new_key = self.keys_map.get(txt[0])
            if new_key:
                film[new_key] = txt[1]
        synopsis = response.selector.xpath(self.all_xpath_rules['synopsis_text']).extract()
        film['synopsis'] = ''.join(synopsis)  # 影片简介.
        m3u8_link = response.selector.xpath(self.all_xpath_rules['m3u8_link']).re_first('https?:(//[^"]+)')
        if m3u8_link:
            film['url'] = m3u8_link
            yield film
            return
        url = response.selector.xpath(self.all_xpath_rules['play_link']).re_first('https?:(//.*)')
        if url:
            req = scrapy.Request('https:%s' % url, callback=self.parse_film_m3u8)
            req.meta['film'] = film
            yield req

    def parse_film_m3u8(self, response):
        film = response.meta['film']
        seletor = scrapy.Selector(text=response.text)
        m3u8_path = None
        for regex in self.m3u8_path_regexs:
            m3u8_path = seletor.re_first(regex)
            if m3u8_path:
                break
        if m3u8_path:
            film['url'] = '//{host}{path}'.format(host=urlparse(response.url).netloc, path=m3u8_path)
        return film

    def parse(self, response):
        for film_link in response.selector.xpath(self.all_xpath_rules['data_list']).extract():
            yield response.follow(film_link, callback=self.parse_film_detail)
        next_page = response.selector.xpath(self.all_xpath_rules['next_page']).extract_first()
        if next_page:
            yield response.follow(next_page)
