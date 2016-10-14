import Vue from 'vue'
import App from './app'

import VueRouter from 'vue-router'
Vue.use(VueRouter)

import Vuex from 'vuex'
Vue.use(Vuex)

import Signup from './comps/signup'
import Index from './comps/index'
import Login from './comps/login'

import ArticlePost from './comps/article-post'

import User from './comps/user'
import Catalog from './comps/catalog'
import Article from './comps/article'

const routes = [
  { path: '/', component: Index },
  { path: '/signup', component: Signup },
  { path: '/login', component: Login },
  { path: '/view/article', component: ArticlePost },
  { path: '/:author', component: User },
  { path: '/:author/:catalog([^\/]+)', component: Catalog },
  { path: '/:author/:catalog([^\/]+)/:name([^\/]+)', component: Article },
  { path: '*', redirect: '/' },
]

// 开发环境下dev server无法正确处理中文URL
let router_config = { routes: routes }
if (typeof webpackHotUpdate === 'undefined') {
  router_config.mode = 'history'
}
const router = new VueRouter(router_config)

// 检查登录状态
router.afterEach(route => {
  res.user.get_me().then(data => {
    console.log(data.username)
  }).catch(() => {
    if (route.path !== '/') {
      router.replace('/login')
    }
  })
})

// 修复Material Design Lite动态效果
router.afterEach(() => {
  router.app.$nextTick(() => {
    componentHandler.upgradeDom()
  })
})

const store = new Vuex.Store({
  state: {
    me: null,
    current_article: null
  },
  mutations: {
    set_me(state, data) {
      state.me = data
    },
    set_current_article(state, data) {
      state.current_article = data
    }
  },
  actions: {
    get_me: context => {
      return res.user.get_me().then(data => {
        context.commit('set_me', data)
        return data
      }).catch(error => {
        console.log(error)
      })
    }
  }
})

import Custom from './custom.js'
Vue.use(Custom, { router: router })


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App),
  directives: {
    marked: function(el, binding) {
      if (binding.value !== undefined) {
        el.innerHTML = marked(binding.value)
      }
    },

  }
})
