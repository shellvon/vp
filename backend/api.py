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
            return filter(None, [self.collect(re.sub('\D', '', link)) for link in links[:self.limit]])
        except Exception as e:
            print('erro occured', e)
            return []

    def _movie_meta_info(self, id, html):
        movie = {
            'id': id,
            'source': self.__class__.__name__,
            'poster': None,
            'url': None
        }
        movie.update({key: ''.join(html.xpath(self.xpath_str_selectors[key])) for key in self.xpath_str_selectors})
        return movie

    def _movie_extra_info(self, id, html):
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

    def _movie_media_info(self, id, html):
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

    def collect(self, id):
        api='{0}?m=vod-detail-id-{1}.html'.format(self.BASE_URI, id)
        html=etree.HTML(self.req.get(api).text)

        movie = self._movie_meta_info(id, html)
        movie.update(self._movie_extra_info(id, html))
        movie.update(self._movie_media_info(id, html))

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


class SkyRjMovie(BaseSpider):
    '''
    这个的搜索貌似只能搜索电影名
    '''
    BASE_URI = 'http://api.skyrj.com'

    def search(self, keyword):
        api = '{}/api/movies'.format(self.BASE_URI)
        movies = self.req.get(api, params={'searchKey': keyword}).json()

        return [self.collect(item['ID']) for item in movies]

    def collect(self, id):
        api = '{}/api/movie'.format(self.BASE_URI)
        resp = self.req.get(api, params={'id': id}).json()

        return self._format(resp)

    def _format(self, item):

        # 导演/主演/介绍是以\n分割..
        def _get(x):
            try:
                return x.split('：')[1]
            except:
                return None
        meta_info = map(_get, item['Introduction'].split('\n'))
        # 按照字母顺序排序
        return {
            'actors': meta_info[1],
            'categories': ','.join(item['Tags'].split('/')),
            'cover': item['Cover'],
            'directors': meta_info[0],
            'download_link': [],
            'id': item['ID'],
            'language': None,
            'name': item['Name'],
            'name_alias': None,
            'note': item['MovieTitle'],
            'play_flash': [],
            'play_m3u8': map(lambda x: {'name': x['Name'], 'url': x['PlayUrl']}, item['MoviePlayUrls']),
            'poster': None,
            'region': None,
            'score': item['Score'],
            'source': self.__class__.__name__,
            'synopsis': meta_info[2],
            'url':  item['MoviePlayUrls'][-1]['PlayUrl'] if item['MoviePlayUrls'] else None,
            'year': item['Year'],
        }


api=Blueprint('api', __name__)

PAGE_ITEM_COUNT = 15

@api.route('/api/suggest')
def suggest():
    endPoint='https://movie.douban.com/j/subject_suggest'
    query=request.args.get('q')
    sug=requests.get(endPoint, params={'q': query}).json()
    return jsonify(sug)

@api.route('/api/search')
def search():
    keyword=request.args.get('keyword')
    feedback = request.args.get('feedback', True, bool)
    crawler=Vip131ZYAPI(PAGE_ITEM_COUNT)
    movies = crawler.search(keyword)
    if not movies and feedback:
        movies = feedback_search(keyword)
    if app.config['EASTER_EGG_ENABLE'] and keyword in app.config['EASTER_EGG_KEYWORDS']:
        movies.insert(0, app.config['EASTER_EGG_MOVIE'])
    return jsonify(movies)

@api.route('/api/movie/<source>/<mid>')
def detail(source, mid):
    movie = {}
    try:
        klass = globals()[source]
        api = klass(PAGE_ITEM_COUNT)
        movie = api.collect(mid)
    except:
        pass
    return jsonify(movie)

def feedback_search(keyword):
    '''此接口由于搜索的比较慢，好处是数据比较多,所以是做为备用的方式提供.'''
    api = SkyRjMovie(PAGE_ITEM_COUNT)
    return api.search(keyword)

if __name__ == "__main__":
    print(feedback_search('越狱'))
