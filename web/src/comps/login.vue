<template lang="html">
  <div class="wrapper">
    <div class="mdl-card mdl-shadow--2dp">
      <div class="mdl-card__title">
        <h3 class="mdl-card__title-text">登录PurePage</h3>
      </div>
      <div class="mdl-card__actions mdl-card--border">
          <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input v-model="form.account" class="mdl-textfield__input" type="text" id="account">
            <label class="mdl-textfield__label" for="account">用户名或邮箱</label>
          </div>
          <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input v-model="form.password" class="mdl-textfield__input" type="password" id="password">
            <label class="mdl-textfield__label" for="password">密码</label>
          </div>
          <button @click="login" class="submit mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored">
            登录
          </button>
          <div class="message"> {{message}} </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.mdl-card {
  margin: 0 auto;
  margin-top: 16px;
  width: 300px + 8px * 2;
}
.mdl-card__title {
  padding: 16px 8px;
}
</style>


<script>
export default {
  data() {
    return {
      form: {},
      message: ''
    }
  },
  methods: {
    login() {
      res.user.post_login(this.form).then(data => {
        this.message = data.message
        this.$router.push('/')
      }).catch(error => {
        this.message = error.message
      })
    }
  }
}
</script>
