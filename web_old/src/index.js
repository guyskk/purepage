import Vue from 'vue'

import Element from 'element-ui'
// import 'element-ui/lib/theme-default/index.css'

import Index from './index.vue'

Vue.use(Element)

new Vue({
    el: '#app',
    render: h => h(Index),
    components: {}
})
