import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import './vuetify'

import 'swiper/dist/css/swiper.css'

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
