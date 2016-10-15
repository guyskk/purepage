<template lang="html">
<div>
  <div class="message">
    {{message}}
  </div>
  <div class="wrapper">
    <div class="article">
      <div v-marked="article.content"></div>
    </div>
    <div class="catalog">
      <ul class="mdl-shadow--4dp">
        <li v-for="item in catalog_articles">
          <a @click="read(item)">{{ item.title }}</a>
        </li>
      </ul>
    </div>
  </div>
</div>
</template>
<script>
export default {
  data() {
    return {
      message:'',
      article:{},
      catalog_articles:[]
    }
  },
  created(){
    this.fetchData()
  },
  watch: {
    // 如果路由有变化，会再次执行该方法
    '$route': 'fetchData'
  },
  methods: {
    fetchData () {
      let {author, catalog, name} =   this.$route.params
      let params = [ author, catalog, name ]
      let aid = params.join('/')
      res.article.get({id:aid}).then(data=>{
        this.article = data
        res.article.get_list({
          author:author,
          catalog: catalog
        }).then(data=>{
          this.catalog_articles = data
        }).catch(error=>{
          this.message = error.message
        })
      }).catch(error=>{
        this.message = error.message
      })
    },
    read(article) {
      this.$store.commit('set_current_article', article)
      this.go(`/${article.author}/${article.catalog}/${article.name}`)
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../assets/variables";
.wrapper {
  display: flex;
}
.article {
  flex: 1;
}
.catalog {
  width: 220px;
  min-height: 320px;
  margin-left: 32px;

  a{
    cursor: pointer;
  }
  ul {
    padding-top: 16px;
    padding-bottom: 16px;
    min-height: 300px;
  }
}

@media (max-width:768px) {
  display: none;
}
</style>
