<template>
<div id="app">
  <img class="logo" src="./assets/logo.png">
  <hello></hello>
  <p>
    Welcome to your Vue.js app!
  </p>
  <p>
    To get a better understanding of how this boilerplate works, check out
    <a href="http://vuejs-templates.github.io/webpack" target="_blank">its documentation</a>. It is also recommended to go through the docs for
    <a href="http://webpack.github.io/" target="_blank">Webpack</a> and
    <a href="http://vuejs.github.io/vue-loader/" target="_blank">vue-loader</a>. If you have any issues with the setup, please file an issue at this boilerplate's
    <a href="https://github.com/vuejs-templates/webpack" target="_blank">repository</a>.
  </p>
  <p>
    You may also want to checkout
    <a href="https://github.com/vuejs/vue-router/" target="_blank">vue-router</a> for routing and
    <a href="https://github.com/vuejs/vuex/" target="_blank">vuex</a> for state management.
  </p>
  <el-button>默认按钮</el-button>
  <el-button type="primary">主要按钮</el-button>
  <el-button type="text">文字按钮</el-button>
</div>
</template>

<script>
import Hello from './components/Hello'
res.user.post_login({
  username: 'root',
  password: '123456'
}).then(user => {
  console.log(user.username)
})

export default {
  components: {
    Hello
  }
}
</script>

<style>
html {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

#app {
  color: #2c3e50;
  margin-top: -100px;
  max-width: 600px;
  font-family: Source Sans Pro, Helvetica, sans-serif;
  text-align: center;
}

#app a {
  color: #42b983;
  text-decoration: none;
}

.logo {
  width: 200px;
  height: 200px
}
</style>
