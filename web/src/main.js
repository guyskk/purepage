import Vue from 'vue'
import App from './app'

import VueRouter from 'vue-router'
Vue.use(VueRouter)

import Vuex from 'vuex'
Vue.use(Vuex)

import Element from 'element-ui'
Vue.use(Element)

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
  routes: routes
})



/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  render: h => h(App)
})
