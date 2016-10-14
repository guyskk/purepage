<template lang="html">
<div class="container">
  <p-header></p-header>
  <div class="message">
    {{message}}
  </div>
  <div class="article">
    <h3>{{ article.title }}</h3>
    <div v-marked="article.content"></div>
  </div>
</div>
</template>
<script>
import Header from './header'

export default {
  data() {
    return {
      message:'',
      article:{},
      params:{}
    }
  },
  components:{
    'p-header': Header
  },
  created(){
    let params = [
      this.$route.params.author,
      this.$route.params.catalog,
      this.$route.params.name
    ]
    let aid = params.join('/')
    res.article.get({id:aid}).then(data=>{
      this.article = data
    }).catch(error=>{
      this.message = error.message
    })
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
@import "../assets/style";
.article {
  width: 100%;
  margin: 0 auto;
}
</style>
