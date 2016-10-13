<template>
<div class="comp">
  <h3>{{article.title}}</h3>
  {{params.username}}/{{params.catalog}}/{{params.article}}
  <div v-marked="article.content"></div>
  <div class="message">
    {{message}}
  </div>
</div>
</template>
<script>

export default {
  data() {
    return {
      message:'',
      article:{},
      params:{}
    }
  },
  created(){
    this.params = this.$route.params
    if(this.$store.state.current_article){
      this.article = this.$store.state.current_article
    }
    res.article.get({id:this.article.id}).then(data=>{
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
@import "../assets/variables";
.comp {
    display: flex;
    flex-direction: column;
    align-items: left;
    padding: 2em;
}

.content {
    width: 100%;
    min-width: 300px;
}

.create {
    color: #fff;
}

</style>
