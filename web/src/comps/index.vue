<template>
<div class="wrapper">
  <div v-for="article in articles" class="card mdl-shadow--2dp">
    <h3 class="card__title">{{ article.title }}</h3>
    <p class="card__summary">{{ article.summary }}</p>
    <div class="card__action">
      <a @click="read(article)"> 继续阅读 </a>
    </div>
  </div>
</div>
</template>

<style lang="scss" scoped>
@import "../assets/variables";
.wrapper {
}
.card {
  width: 100%;
  margin-top: 16px;
  padding: 8px;
}
.card__summary {
  min-height: 48px;
  padding-left: 16px;
  padding-right: 16px;
}
.card__title {
  color: $color-teal;
  background: #fff;
}
.card__action {
  a {
    color: $color-teal;
    cursor: pointer;
    margin-left: 16px;
  }
}
</style>
<script>
import Header from './header'
export default {
  data() {
    return {
      articles:[]
    }
  },
  components:{
    'p-header': Header
  },
  methods: {
    read(article) {
      this.$store.commit('set_current_article', article)
      this.go(`/${article.author}/${article.catalog}/${article.name}`)
    }
  },
  created(){
    res.article.get_top().then(data=>{
      for(let x of data){
        this.articles.push(x)
      }
    })
  }
}
</script>
