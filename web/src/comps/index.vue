<template>
<div class="index">
  <img class="logo" src="../assets/logo.png">
  <el-row :gutter="20">
    <el-col :span="12">
      <el-button type="primary" @click.native="$router.push('/login')">
        登录
      </el-button>
    </el-col>
    <el-col :span="12">
      <el-button type="success" @click.native="$router.push('/signup')">
        注册
      </el-button>
    </el-col>
  </el-row>
</div>
</template>

<script>
export default {
  data() {
    return {
      msg: 'Hello Vue!'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a {
  color: #fff;
  text-decoration: none;
}

.logo {
  max-width: 320px;
  max-height: 320px;
}

.el-button {
  width: 100%;
}
</style>
