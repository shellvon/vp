<template>
  <v-app id="app">
    <v-content>
      <transition :name="transitionName" @afterLeave="clearTransition">
      <v-container id="container">
        <router-view></router-view>
      </v-container>
      </transition>
    </v-content>
  </v-app>
</template>

<script>

import {mapState} from 'vuex';
import store from './store';

export default {
  name: 'app',
  data() {
    return {
      prevRoute:''
    }
  },
  computed: {
    ...mapState('transition', ['transitionName']),
  },
  methods: {
    clearTransition()
    {
      store.commit('transition/setTransition', '')
    }
  },
  watch: {
    $route(to, from) {
      if (!(to.meta.noPageAnimation || from.meta.noPageAnimation)) {
        if (to.name === this.prevRoute) {
          store.commit('transition/setTransition', 'turn-off');
        } else if (from.name != null) {
          store.commit('transition/setTransition', 'turn-on');
          this.prevRoute = from.name
        }
      }
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* background-color: #f5f5f5;
  margin-top: 60px; */
}
#container {
  max-width: 550px;
  pad: 8px;
}
</style>
