# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask import request
import re
from lxml import etree
import requests



BASE_URI = 'http://www.zuidazy.net/'


class ZuidaZYAPI(object):
    def __init__(self, limit=10):
        self.req = requests.Session()
        self.limit = limit # 单词最多返回多少搜索结果

    def search(self, keyword):
        api = '{0}index.php?m=vod-search'.format(BASE_URI)
        try:
            data = self.req.post(api, data={'wd': keyword}).text
            links = re.findall('\?m=vod-detail-id-\d+.html', data)
            return filter(None, [self.collect(link) for link in links[:self.limit]])
        except Exception as e:
            print('erro occured', e)
            return []

    def collect(self, item):
        api = '{0}{1}'.format(BASE_URI, item)
        html = etree.HTML(self.req.get(api).text)

        movie_base_info = {
            'id': 'zuidazy_{}'.format(re.sub('\D', '', item)),
            'source': 'http://www.zuidazy.net/',
            'poster': None,
            'cover': html.xpath('//div[@class="vodImg"]/img/@src')[0],

        }

        movie_attr_xpath_map = {
            'cover': '//div[@class="vodImg"]/img/@src',  # 封面
            'name': '//div[@class="vodInfo"]/div/h2/text()',  # 电影名
            'note': '//div[@class="vodInfo"]/div/span/text()',  # 备注(BD高清等)
            'score': '//div[@class="vodInfo"]/div/label/text()',  # 分数
            'synopsis': '(//div[@class="vodplayinfo"])[2]/text()'  # 剧情简介
        }

        movie_meta_info = {
            key: html.xpath(movie_attr_xpath_map[key])[0]
            for key in movie_attr_xpath_map
        }

        # 别名/导演/演员等信息在这个ul里面,所以顺序很重要
        meta_info = html.xpath('//div[@class="vodinfobox"]/ul/li/span')
        movie_additional_info = {
            key: meta_info[index].text for (index, key) in enumerate(['name_alias',
                                                               'directors',
                                                               'actors',
                                                               'categories',
                                                               'region',
                                                               'language',
                                                               'year'])}
        movie = dict(movie_base_info, **dict(movie_meta_info, **movie_additional_info))

        def mapper(s):
            k,v = s.split('$')
            return {'name': k, 'url': v}
        # 更新播放地址/下载地址
        movie.update(
            {
                'download_link': map(mapper, html.xpath('//div[@class="vodplayinfo"]/div/div[@id="down_1"]/ul/li/text()')),
                'play_m3u8': map(mapper, html.xpath('//div[@class="vodplayinfo"]/div/div[@id="play_1"]/ul/li/text()')),
                'play_flash': map(mapper,html.xpath('//div[@class="vodplayinfo"]/div/div[@id="play_2"]/ul/li/text()')),
            }
        )
        # 默认播放地址
        movie['url']  = movie['play_flash'][-1]['url'] if movie['play_flash'] else None
        return movie

api = Blueprint('api', __name__)
crawler = ZuidaZYAPI(10)

@api.route('/api/suggest')
def suggest():
    endPoint = 'https://movie.douban.com/j/subject_suggest'
    query = request.args.get('q')
    sug = requests.get(endPoint, params={'q': query}).json()
    return jsonify(sug)

@api.route('/api/search')
def search():
    keyword = request.args.get('keyword')

    return jsonify(crawler.search(keyword))

