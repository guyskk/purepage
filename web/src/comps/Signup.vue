<template lang="html">
  <div class="signup">
    <h2>注册PurePage</h2>
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" placeholder="用户名"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" placeholder="密码"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" placeholder="邮箱可选"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" class="submit" @click.native="onSubmit">注册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style lang="css">
.signup{
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
        email: [{
          required: false,
          message: '邮箱',
          trigger: 'blur'
        }]
      }

    }
  },
  methods: {
    onSubmit() {
      console.log("xxx")
      res.user.post_signup(this.form).then(data => {
        this.$alert(data.message);
      }).catch(error => {
        this.$alert(error.message);
      })
    }
  }
}
</script>
