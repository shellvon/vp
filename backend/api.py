# -*- coding:utf-8 -*-

import re
import time
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import current_app as app
from lxml import etree
import requests
from functools import partial
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


def worker(obj, method, *args, **kwargs):
    return getattr(obj, method)(*args, **kwargs)


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
            pool = Pool()
            collect_worker = partial(worker, self, 'collect')
            jobs = [pool.map_async(collect_worker, (re.sub(
                '\D', '', link), )) for link in links[:self.limit]]
            pool.close()
            pool.join()
            return [item[0] for item in (job.get() for job in jobs) if item and item[0]]

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
        movie.update({key: ''.join(html.xpath(
            self.xpath_str_selectors[key])) for key in self.xpath_str_selectors})
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
            key: ''.join(extra_info[index].xpath('text()')).strip() for (index, key) in enumerate(extra_info_keys)
        }

    def _movie_media_info(self, id, html):
        def to_dict(source):
            try:
                key, val = source.split('$')
            except:
                key = val = source
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
        api = '{0}?m=vod-detail-id-{1}.html'.format(self.BASE_URI, id)
        html = etree.HTML(self.req.get(api).text)

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
        try:
            movies = self.req.get(api, params={'searchKey': keyword}).json()
        except Exception as e:
            print('Skymovie search error', e)
            return []
        pool = Pool()
        collect_worker = partial(worker, self, 'collect')

        jobs = [pool.map_async(delay(collect_worker, 0.1), (item['ID'], ))
                for item in movies]
        pool.close()
        pool.join()
        return [item[0] for item in (job.get() for job in jobs) if item and item[0]]

    def collect(self, id):
        api = '{}/api/movie'.format(self.BASE_URI)
        try:
            resp = self.req.get(api, params={'id': id}).json()
        except Exception as e:
            return None
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


class Aiwan94(BaseSpider):
    BASE_URI = 'http://www.94aw.com/'

     # 返回字符串的选择器
    xpath_str_selectors = {
        'cover': '//img[@class="img-thumbnail"]/@src',  # 封面
        'name': '//h1[@class="movie-title"]/text()',  # 电影名
        'note': '//button[@class="hdtag"]/text()',  # 备注(BD高清等)
        'score': '//a[@class="score"]/text()',  # 分数
        'synopsis': '//p[@class="summary"]/text()'  # 剧情简介
    }

    # 返回数组的选择器
    xpath_lst_selectors = {
        # 别名/导演/演员等信息在这个ul里面,所以顺序很重要
        'extra': '//table/tbody/tr/td[2]',
        # flash播放地址
        'play_flash': '//ul[@class="dslist-group"]/li/a',
    }

    def search(self, keyword):
        try:
            resp = self.req.get('{0}search'.format(self.BASE_URI), params={'wd': keyword})
            resp.encoding='utf-8'
            data = resp.text
            links = list(set(re.findall('/show/(\d+).html', data)))
            pool = Pool()
            collect_worker = partial(worker, self, 'collect')
            jobs = [pool.map_async(collect_worker, (re.sub(
                '\D', '', link), )) for link in links[:self.limit]]
            pool.close()
            pool.join()
            return [item[0] for item in (job.get() for job in jobs) if item and item[0]]

        except Exception as e:
            print('erro occured', e)
            return []

    def collect(self, id):
        api = '{0}show/{1}.html'.format(self.BASE_URI, id)
        resp = self.req.get(api)
        resp.encoding='utf-8'
        html = etree.HTML(resp.text)
        movie = self._movie_meta_info(id, html)
        movie.update(self._movie_extra_info(id, html))
        movie.update(self._movie_media_info(id, html))
        return movie

    def _movie_extra_info(self, id, html):
        extra_info = html.xpath(self.xpath_lst_selectors['extra'])
         # Order is very important
        extra_info_keys = [
            'directors',
            'actors',
            'categories',
            'region',
            'note',
            'year'
        ]
        return {
            key: ''.join(extra_info[index].xpath('text()')).strip() for (index, key) in enumerate(extra_info_keys)
        }

    def _movie_media_info(self, id, html):
        lst = []
        for el in html.xpath(self.xpath_lst_selectors['play_flash']):
            try:
                detail = self.req.get('{0}{1}'.format(self.BASE_URI, el.get('href'))).text
                src = etree.HTML(detail).xpath('//iframe/@src')[0]
                lst.append(
                    {
                        'name':  el.xpath('text()')[0].strip('/'),
                        'url':   src.replace('https://apis.tianxianle.com', '')
                    }
                )
            except:
                pass

        media_info = {
            'play_m3u8': [],
            'play_flash': lst,
            'download_link': [],
        }
        # set default
        media_info['url'] = media_info['play_flash'][-1]['url'] if media_info['play_flash'] else None
        return media_info


class NiuZy(BaseSpider):
    BASE_URI = 'https://www.niuzy.cc/'
    # 返回数组的选择器
    xpath_lst_selectors = {
        # 别名/导演/演员等信息在这个ul里面,所以顺序很重要
        'extra': '//div[@class="vodinfobox"]/ul/li/span',
        # 下载地址
        'download_link': '//div[@class="vodplayinfo"]/div/div[@id="down_1"]/ul/li/text()',
        # m3u8播放地址
        'play_m3u8': '//div[@class="vodplayinfo"]/div/ul[1]/li/text()',
        # flash播放地址
        'play_flash': '//div[@class="vodplayinfo"]/div/ul[2]/li/text()',
    }

    def search(self, keyword):
        params = {
            'wd': keyword,
            'submit': 'search'
        }
        data = self.req.get('{0}vodsearch/-------------/'.format(self.BASE_URI), params=params).text
        movie_ids = re.findall('/voddetail/(\d+)/', data)
        pool = Pool()
        collect_worker = partial(worker, self, 'collect')
        jobs = [pool.map_async(collect_worker, (id,)) for id in movie_ids[:self.limit]]
        pool.close()
        pool.join()
        return [item[0] for item in (job.get() for job in jobs) if item and item[0]]

    def collect(self, id):
        api = '{0}/voddetail/{1}'.format(self.BASE_URI, id)
        html = etree.HTML(self.req.get(api).text)
        movie = self._movie_meta_info(id, html)
        movie.update(self._movie_extra_info(id, html))
        movie.update(self._movie_media_info(id, html))

        return movie


class JingpinZy(BaseSpider):
    BASE_URI = 'http://www.jingpinzy.com/'

    # 返回字符串的选择器
    xpath_str_selectors = {
        'cover': '//div[@class="videoPic"]/img/@src',  # 封面
        # 'name': '//div[@class="videoDetail"]/li/text()',  # 电影名
        # 'note': '//div[@class="vodInfo"]/div/span/text()',  # 备注(BD高清等)
        # 'score': '//div[@class="vodInfo"]/div/label/text()',  # 分数
        'synopsis': '(//div[@class="movievod"]/p)[2]/text()'  # 剧情简介
    }

    # 返回数组的选择器
    xpath_lst_selectors = {
        # 别名/导演/演员等信息在这个ul里面,所以顺序很重要
        'extra': '//div[@class="videoDetail"]/li[@class="sa"]|//div[@class="videoDetail"]/li/div',
        # 下载地址
        'download_link': '//div[@class="vodplayinfo"]/div/ul/li/text()',
        # m3u8播放地址
        'play_m3u8': '//div[@class="movievod"]/ul/li[2]/input/@value',
        # flash播放地址
        'play_flash': '//div[@class="movievod"]/ul/li[4]/input/@value',
    }


    def collect(self, id):
        data = self.req.get(self.BASE_URI, params = {'m': 'vod-detail-id-{0}.html'.format(id)}).text
        html = etree.HTML(data)
        movie = self._movie_meta_info(id, html)
        movie.update(self._movie_extra_info(id, html))
        movie.update(self._movie_media_info(id, html))

        return movie

    def _movie_meta_info(self, id, html):
        movie = {
            'id': id,
            'source': self.__class__.__name__,
            'poster': None,
            'url': None
        }
        movie.update({key: ''.join(html.xpath(
            self.xpath_str_selectors[key])) for key in self.xpath_str_selectors})
        return movie

    def _movie_extra_info(self, id, html):
        extra_info = html.xpath(self.xpath_lst_selectors['extra'])
        extra_info_keys = [
            'name',
            'alias',
            'note',
            'actors',
            'directors',
            'categories',
            '-',
            'language',
            'region',
            '-',
            'year',
            '-',
            'score'
        ]
        data = {
            key: re.sub('^([^:]+:\s*)', '', ''.join(extra_info[index].xpath('text()'))) for (index, key) in enumerate(extra_info_keys) if key != '-'
        }
        return data

    def _movie_media_info(self, id, html):
        def to_dict(source):
            try:
                key, val = source.split('$')
            except:
                key = val = source
            return {'name': key, 'url': val}

        m3u8 = map(to_dict, html.xpath(self.xpath_lst_selectors['play_m3u8']))
        flash = map(to_dict, html.xpath(self.xpath_lst_selectors['play_flash']))
        if flash and flash[0]['url'].endswith('.m3u8'):
            m3u8,flash = flash, m3u8
        if m3u8 and not m3u8[0]['url'].endswith('.m3u8'):
            m3u8,flash = flash, m3u8
        media_info = {
            'play_m3u8': m3u8,
            'play_flash': flash,
            'download_link': map(to_dict, html.xpath(self.xpath_lst_selectors['download_link']))
        }
        media_info['url'] = media_info['play_flash'][-1]['url'] if media_info['play_flash'] else None
        return media_info

api = Blueprint('api', __name__)

PAGE_ITEM_COUNT = 15

def delay(worker, period):
    '''搜索的商户频率太快会Connection Refused,所以需要延迟那么一会儿'''
    time.sleep(period)
    return worker

@api.route('/api/suggest')
def suggest():
    endPoint = 'https://movie.douban.com/j/subject_suggest'
    query = request.args.get('q')
    sug = requests.get(endPoint, params={'q': query}).json()
    return jsonify(sug)


@api.route('/api/search')
def search():
    keyword = request.args.get('keyword')
    movies = multi_search(keyword)
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


def multi_search(keyword):
    spider_tables = [
        # Vip131ZYAPI,
        # ZuidaZYAPI,
        JingpinZy,
        Aiwan94,
    ]
    thread_pool = ThreadPool()
    jobs = [thread_pool.map_async(partial(worker, cls(
        PAGE_ITEM_COUNT), 'search'), (keyword, )) for cls in spider_tables]
    results = [job.get() for job in jobs]
    thread_pool.close()
    thread_pool.join()

    movies = []
    for ret in results:
        movies.extend(ret[0] if ret else [])
    return movies


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')
    spider = JingpinZy(10)

    print spider.collect('20173')