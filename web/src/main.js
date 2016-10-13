import Vue from 'vue'
import App from './app'

import VueRouter from 'vue-router'
Vue.use(VueRouter)

import Vuex from 'vuex'
Vue.use(Vuex)

import Signup from './comps/signup'
import Index from './comps/index'
import Login from './comps/login'
import Article from './comps/article'

const routes = [
  { path: '/', component: Index },
  { path: '/signup', component: Signup },
  { path: '/login', component: Login },
  { path: '/view/article', component: Article },
  { path: '*', redirect: '/' },
]

const router = new VueRouter({
  mode: 'history',
  routes: routes,
})

// 检查登录状态
router.afterEach(() => {
  res.user.get_me().then(data => {
    console.log(data.username)
  }).catch(() => {
    router.replace('/login')
  })
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
  render: h => h(App)
})
