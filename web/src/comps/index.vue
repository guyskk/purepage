<template>
<div class="container">
  <p-header></p-header>
  <main>
    <div v-for="article in articles" class="mdl-card mdl-shadow--2dp">
      <div class="mdl-card__title">
        <h3 class="mdl-card__title-text">{{ article.title }}</h3>
      </div>
      <div class="mdl-card__supporting-text">
        {{ article.summary }}
      </div>
      <div class="mdl-card__actions mdl-card--border">
        <a @click="read(article)" class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect">
          继续阅读
        </a>
      </div>
    </div>
  </main>
</div>
</template>

<style lang="scss" scoped>
@import "../assets/style";
.mdl-card {
  width: 100%;
  margin-top: 16px;
}
.mdl-card > .mdl-card__title {
  color: $color-teal;
  background: #fff;
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
