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
console.log('x')
export default {
  data() {
    return {
      message:'',
      article:{},
      params:{}
    }
  },
  created(){
    console.log('x')
    this.params = this.$route.params
    if(this.$store.state.current_article){
      this.article = this.$store.state.current_article
    }else{
      let params = [this.params.author,this.params.catalog,this.params.name]
      console.log(params)
      this.article = {id:params.join('/')}
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
