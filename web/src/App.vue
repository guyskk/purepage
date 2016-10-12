<template>
<div id="app">
  <img class="logo" src="./assets/logo.png">
  <signup></signup>
</div>
</template>

<script>
import Signup from './comps/Signup'

export default {
  components: {
    Signup
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
  max-width: 1200px;
  text-align: center;
}

.logo {
  width: 200px;
  height: 200px
}
</style>
