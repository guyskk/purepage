<template>
<div class="comp">
  <img class="logo" src="/static/logo.png">
  <div class="action">
    <button @click="go('/login')" class="login mdl-button mdl-js-button mdl-button--raised">
      登录
    </button>
    <button @click="go('/signup')" class="signup mdl-button mdl-js-button mdl-button--raised">
      注册
    </button>
  </div>
  <br>
  <div class="article" v-for="article in articles">
    <div class="article-card mdl-card mdl-shadow--2dp">
      <div class="mdl-card__title">
        <h2 class="mdl-card__title-text">{{ article.title }}</h2>
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
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      articles:[]
    }
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

<style lang="scss" scoped>@import "../assets/variables";
.comp {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.logo {
    width: 320px;
    height: 320px;
}

.action {
    display: flex;
    width: 320px;
}

.action button {
    flex: 1;
    margin: 0 10px;
    color: #fff;
}

.login {
    background-color: $color-teal;
}
.signup {
    background-color: $color-green;
}

.article-card,
.mdl-card {
    width: 100%;
    min-width: 320px;
    margin-top: 16px;
}
.article-card > .mdl-card__title {
    color: #fff;
    height: 64px;
    background: $color-teal;
}
.article-card > .mdl-card__menu {
    color: #fff;
}
</style>
