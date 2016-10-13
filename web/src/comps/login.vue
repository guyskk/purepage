<template lang="html">
  <div class="login">
    <h2 class="header">登录PurePage</h2>
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="帐号" prop="username">
        <el-input v-model="form.username" placeholder="用户名或邮箱"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" placeholder="密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" class="submit" @click.native="login">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style lang="css">
.header {
  text-align: center;
}
.login{
  margin-top: 160px;
  width: 400px;
}
.submit{
  width: 100%;
}
</style>


<script>
export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
        email: ''
      },
      rules: {
        username: [{
          required: true,
          message: '请输入用户名',
          trigger: 'blur'
        }],
        password: [{
          required: true,
          message: '请输入密码',
          trigger: 'blur'
        }],
      }
    }
  },
  methods: {
    login() {
      res.user.post_login(this.form).then(data => {
        this.$alert(`Welcome ${data.username}!`);
      }).catch(error => {
        this.$alert(error.message);
      })
    }
  }
}
</script>
