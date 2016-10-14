<template lang="html">
  <header class="header">
    <div class="logo">
      <img @click="go('/')" src="/static/logo.png">
    </div>
    <div class="action">
      <button @click="go('/view/article')" class="create mdl-button mdl-js-button mdl-button--raised">
        创作
      </button>
      <button @click="go('/login')" class="login mdl-button mdl-js-button mdl-button--raised">
        登录
      </button>
      <button @click="go('/signup')" class="signup mdl-button mdl-js-button mdl-button--raised">
        注册
      </button>
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
@import "../assets/style";
.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  border-bottom: 1px solid #f1f1f1;
}
.logo img{
    width: 60px;
    height: 60px;
    cursor: pointer;
}
.action {
    display: flex;
}
.action button {
    flex: 1;
    margin-left: 20px;
    color: #fff;
}
.login {
    background-color: $color-teal;
}
.signup {
    background-color: $color-green;
}
.create {
  background-color: $color-green;
}
</style>
