var commentObj = function(){
	this.btn;
	this.text;
	this.textCon;
}
commentObj.prototype.init = function(){
	this.btn = getDom('comment-btn');
	this.text = '';
	this.textCon = getDom('textCon');
	this.btn.addEventListener('click',function(){
		com.postCom();
	},false);
}
commentObj.prototype.postCom = function(){
	this.text = getDom('textCon').value;
	if(this.text.length <= 2){
		alert('您输入的评论太短');
	}
  else if(this.text.length >= 150){
    alert('您输入的评论太长');
  }
	else{
    this.text = getDom('textCon').value.toString();
		res.comment.post({
      article_id: comment.artId,
      content: this.text
		}).then(function(data) {
      console.log(data);
    }).catch(function(err) {
      console.log(err);
    })
	}
}

var com;
var title;
var comment;
var url;
var userid;
var catalog;
var article;

document.body.onload = game;

function game(){
  load();
  com = new commentObj();
  com.init();
  title = new Vue({
    el: "#scripts",
    data: {
      pageTitle: '',
      pageScript: '',
    }
  });
  comment = new Vue({
    el: "#othersCom",
    data: {
      artId: '',
      num: 0
    }
  })
  url = location.pathname.split('/');
  userid = decodeURI(url[1]);
  catalog = decodeURI(url[2]);
  article = decodeURI(url[3]);
  title.pageTitle = article;
  //获取文章
  res.article.get({
    article: article,
    catalog: catalog,
    userid: userid
  }).then(function(data) {
    console.log(data);
    var newArt = document.createElement('div');
    newArt.className = 'markdown-body';
    newArt.innerHTML = data.content;
    document.getElementById('blogArt').appendChild(newArt);
    comment.artId = unescape(article);
    // comment.num = data.rows.length;
    console.log(article);
    //获取评论
    res.comment.get({
      article: comment.artId
    }).then(function(data) {
      console.log(data);
      comment.num = data.rows.length;
    }).catch(function(err) {
      console.log(err);
    })
  }).catch(function(err) {
    console.log(err);
  })
}
