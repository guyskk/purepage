<template lang="html">
  <div class="wrapper">
    <div class="mdl-card mdl-shadow--2dp">
      <div class="mdl-card__title">
        <h3 class="mdl-card__title-text">注册PurePage</h3>
      </div>
      <div class="mdl-card__actions mdl-card--border">
          <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input v-model="form.id" class="mdl-textfield__input" type="text" id="id">
            <label class="mdl-textfield__label" for="id">用户名</label>
          </div>
          <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input v-model="form.password" class="mdl-textfield__input" type="text" id="password">
            <label class="mdl-textfield__label" for="password">密码</label>
          </div>
          <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input v-model="form.email" class="mdl-textfield__input" type="text" id="email">
            <label class="mdl-textfield__label" for="email">邮箱可选</label>
          </div>
          <button @click="signup" class="submit mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored">
            注册
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
      message: '',
    }
  },
  methods: {
    signup() {
      res.user.post_signup(this.form).then(data => {
        this.message = data.message
        this.$router.push('/login')
      }).catch(error => {
        this.message = error.message
      })
    }
  }
}
</script>
