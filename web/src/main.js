import Vue from 'vue'
import App from './app'

import VueRouter from 'vue-router'
Vue.use(VueRouter)

import Vuex from 'vuex'
Vue.use(Vuex)

import Signup from './comps/signup'
import Index from './comps/index'
import Login from './comps/login'

const routes = [
  { path: '/', component: Index },
  { path: '/signup', component: Signup },
  { path: '/login', component: Login },
  { path: '*', redirect: '/' },
]

const router = new VueRouter({
  mode: 'history',
  routes: routes,
})

// 修复Material Design Lite动态效果
router.afterEach(() => {
  router.app.$nextTick(() => {
    componentHandler.upgradeDom()
  })
})


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  render: h => h(App),
  methods: {
    go(url) {
      this.$router.push(url)
    }
  }
})
