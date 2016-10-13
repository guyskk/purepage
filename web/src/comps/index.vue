<template>
<div class="comp">
  <img class="logo" src="/static/logo.png">
  <div class="action">
    <button @click="go('/login')" class="login mdl-button mdl-js-button mdl-button--raised">
      登录
    </button>
    <button @click="go('/signup')" class="signup mdl-button mdl-js-button mdl-button--raised">
      注册
    </button>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      msg: 'Hello Vue!'
    }
  },
  methods: {
    go(url) {
      this.$router.push(url)
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../assets/variables";
.comp {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.logo {
    width: 320px;
    height: 320px;
}

.action {
    display: flex;
    width: 320px;
}

.action button {
    flex: 1;
    margin: 0 10px;
    color: #fff;
}

.login {
    background-color: $color-teal;
}
.signup {
    background-color: $color-green;
}
</style>
