<template>
<div class="wrapper">
  <h3>创建文章</h3>
  <div class="meta">
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <input v-model="article.name" class="mdl-textfield__input" type="text" id="name">
      <label class="mdl-textfield__label" for="name">名称</label>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <input v-model="article.title" class="mdl-textfield__input" type="text" id="title">
      <label class="mdl-textfield__label" for="title">标题</label>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <input v-model="article.catalog" class="mdl-textfield__input" type="text" id="catalog">
      <label class="mdl-textfield__label" for="catalog">目录</label>
    </div>
  </div>
  <div class="content">
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <textarea v-model="article.summary" class="mdl-textfield__input" type="text" rows="3" id="summary"></textarea>
      <label class="mdl-textfield__label" for="summary">摘要</label>
    </div>
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
      <textarea v-model="article.content" class="mdl-textfield__input" type="text" rows="15" id="content" ></textarea>
      <label class="mdl-textfield__label" for="content">Markdown here</label>
    </div>
  </div>
  <button @click="create" class="create submit mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored">
    创建文章
  </button>
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
      article:{
        tags:[]
      }
    }
  },
  methods: {
    create() {
      res.article.post(this.article).then(data=>{
        this.message = data.id
      }).catch(error=>{
        this.message = error.message
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../assets/variables";
.meta {
  width: 316px;
}
.content {
  width: 100%;
  .mdl-textfield {
    width: 100%;
  }
}
.create {
    color: #fff;
}

</style>
