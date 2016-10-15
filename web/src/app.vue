<template>
<div class="container">
  <p-header></p-header>
  <router-view></router-view>
</div>
</template>

<script>
import Header from './comps/header'
export default {
  components:{
    'p-header': Header
  }
}
</script>

<style lang="scss">
@import "./assets/style";
</style>
