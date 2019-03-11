import request from '@/utils/request'

export function suggest(q) {
    return request({
        url: 'api/suggest',
        method: 'GET',
        params: {
            q
        }
    })
}

export function search(keyword) {
    return request({
        url: 'api/search',
        method: 'GET',
        params: {
            keyword
        }
    })
}

export function detail(source, movieId){
    return request({
        url: `/api/movie/${source}/${movieId}`
    })
}

export function getHotSearch(){
    return request({
        url: '/api/movie/hot-search'
    })
}