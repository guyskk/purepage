<template lang="html">
<div>
  <div class="message">
    {{message}}
  </div>
  <div class="wrapper">
    <div class="article">
      <h3>{{ article.title }}</h3>
      <div v-marked="article.content"></div>
    </div>
    <div class="catalog">

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
      params:{}
    }
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
  background: #f1f1f1;
  margin-left: 32px;
}

@media (max-width:768px) {
  display: none;
}
</style>
