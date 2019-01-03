import axios from 'axios';

const service = axios.create({
    baseURL: process.env.VUE_APP_BASE_API,
    timeout: 60000
})


service.interceptors.response.use(response => {
    const res = response.data;
    if (res.code && res.code !== 200) {
        return Promise.reject('error')
    }
    return response.data
}, (error) => {
    // Toast ???
    return Promise.reject(error)
})

export default service;