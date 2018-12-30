# -*- coding:utf-8 -*-

import re
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import current_app as app
from lxml import etree
import requests



class BaseSpider(object):

    BASE_URI = 'http://www.zuidazy.net/'

    # 返回字符串的选择器
    xpath_str_selectors = {
        'cover': '//div[@class="vodImg"]/img/@src',  # 封面
        'name': '//div[@class="vodInfo"]/div/h2/text()',  # 电影名
        'note': '//div[@class="vodInfo"]/div/span/text()',  # 备注(BD高清等)
        'score': '//div[@class="vodInfo"]/div/label/text()',  # 分数
        'synopsis': '(//div[@class="vodplayinfo"])[2]/text()'  # 剧情简介
    }

    # 返回数组的选择器
    xpath_lst_selectors = {
        # 别名/导演/演员等信息在这个ul里面,所以顺序很重要
        'extra': '//div[@class="vodinfobox"]/ul/li/span',
        # 下载地址
        'download_link': '//div[@class="vodplayinfo"]/div/div[@id="down_1"]/ul/li/text()',
        # m3u8播放地址
        'play_m3u8': '//div[@class="vodplayinfo"]/div/div[@id="play_1"]/ul/li/text()',
        # flash播放地址
        'play_flash': '//div[@class="vodplayinfo"]/div/div[@id="play_2"]/ul/li/text()',
    }

    def __init__(self, limit=10):
        self.limit = limit
        self.req = requests.Session()

    def search(self, keyword):
        api = '{0}index.php?m=vod-search'.format(self.BASE_URI)
        try:
            data = self.req.post(api, data={'wd': keyword}).text
            links = re.findall('\?m=vod-detail-id-\d+.html', data)
            return filter(None, [self.collect(link) for link in links[:self.limit]])
        except Exception as e:
            print('erro occured', e)
            return []

    def _movie_meta_info(self, item, html):
        movie = {
            'id': re.sub('\D', '', item)[0],
            'source': '{0}{1}'.format(self.BASE_URI, item),
            'poster': None,
            'url': None
        }
        movie.update({key: ''.join(html.xpath(self.xpath_str_selectors[key])) for key in self.xpath_str_selectors})
        return movie

    def _movie_extra_info(self, item, html):
        extra_info = html.xpath(self.xpath_lst_selectors['extra'])
        # Order is very important
        extra_info_keys = [
            'name_alias',
            'directors',
            'actors',
            'categories',
            'region',
            'language',
            'year'
        ]
        return {
            key: ''.join(extra_info[index].xpath('text()')) for (index, key) in enumerate(extra_info_keys)
        }

    def _movie_media_info(self, item, html):
        def to_dict(source):
            key, val = source.split('$')
            return {'name': key, 'url': val}
        media_info = {
            'play_m3u8': map(to_dict, html.xpath(self.xpath_lst_selectors['play_m3u8'])),
            'play_flash': map(to_dict, html.xpath(self.xpath_lst_selectors['play_flash'])),
            'download_link': map(to_dict, html.xpath(self.xpath_lst_selectors['download_link']))
        }
        # set default
        media_info['url'] = media_info['play_flash'][-1]['url'] if media_info['play_flash'] else None
        return media_info

    def collect(self, item):
        api='{0}{1}'.format(self.BASE_URI, item)
        html=etree.HTML(self.req.get(api).text)

        movie = self._movie_meta_info(item, html)
        movie.update(self._movie_extra_info(item, html))
        movie.update(self._movie_media_info(item, html))

        return movie


class ZuidaZYAPI(BaseSpider):
    BASE_URI = 'http://www.zuidazy.net/'


class Vip131ZYAPI(BaseSpider):
    BASE_URI = 'http://131zy.vip/'
     # 返回数组的选择器
    xpath_lst_selectors = {
        # 别名/导演/演员等信息在这个ul里面,所以顺序很重要
        'extra': '//div[@class="vodinfobox"]/ul/li/span',
        # 下载地址
        'download_link': '//div[@class="vodplayinfo"]/div/div[@id="down_1"]/ul/li/text()',
        # m3u8播放地址
        'play_m3u8': '//div[@class="vodplayinfo"]/div/ul[2]/li/text()',
        # flash播放地址
        'play_flash': '//div[@class="vodplayinfo"]/div/ul[1]/li/text()',
    }

api=Blueprint('api', __name__)

crawler=Vip131ZYAPI(15)

@api.route('/api/suggest')
def suggest():
    endPoint='https://movie.douban.com/j/subject_suggest'
    query=request.args.get('q')
    sug=requests.get(endPoint, params={'q': query}).json()
    return jsonify(sug)

@api.route('/api/search')
def search():
    keyword=request.args.get('keyword')
    movies = crawler.search(keyword)
    if app.config('EASTER_EGG_ENABLE'):
        movies.append(app.config('EASTER_EGG_MOVIE'))
    return jsonify(movies)
