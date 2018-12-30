import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router)

const router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            redirect: '/home'
        },
        {
            path: '/home',
            name: 'home',
            component(resolve) {
                require(['@/views/home/index.vue'], resolve)
            }
        },
        {
            path: '/player',
            name: 'player',
            component(resolve) {
                require(['@/views/movie/player.vue'], resolve)
            }
        }
    ]
})

export default router;