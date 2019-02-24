import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import uweb from 'vue-uweb'
import './vuetify'

import 'swiper/dist/css/swiper.css'

Vue.config.productionTip = false
Vue.use(uweb, {siteId: '1276245163', src: '//s5.cnzz.com/z_stat.php?id=1276245163&online=1&show=line'})

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
