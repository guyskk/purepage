<template lang="html">
  <header class="header">
    <div class="logo">
      <img @click="go('/')" src="/static/logo.png">
    </div>
    <div class="action">
      <a href="/api">API文档</a>
      <a @click="go('/view/article')">创作</a>
      <a @click="go('/login')">登录</a>
      <a @click="go('/signup')">注册</a>
    </div>
  </header>
</template>

<script>
export default {
  data () {
    return {}
  },
  computed: {},
  ready () {},
  attached () {},
  methods: {},
  components: {}
}
</script>

<style lang="scss" scoped>
@import "../assets/variables";
.header {
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  border-bottom: 1px solid #f1f1f1;
  width: 100%;
  height: 60px;
}
.logo img{
    width: 60px;
    height: 60px;
    cursor: pointer;
}
.action {
    display: flex;
    align-items: center;
}
.action a {
    margin-left: 20px;
    cursor: pointer;
}
</style>
