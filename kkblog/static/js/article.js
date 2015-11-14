$(window).ready(function() {
	var url = decodeURI(location.pathname)

	function parse_article_url(url) {
		var r = "^.*/(.+)/(.+)/(.+)$";
		var rex = RegExp(r);
		var result = rex.exec(url);
		if (!result || result.length < 4) {
			throw "can't parse article url: " + url;
		}
		return {
			"gitname": result[1],
			"subdir": result[2],
			"filename": result[3] + ".md",
		}
	};

	var get_article_info = parse_article_url(url);
	//通过三个参数确定唯一的文章
	res.api.article.get({
		"filename": get_article_info.filename,
		"gitname": get_article_info.gitname,
		"subdir": get_article_info.subdir,
	}, function(error, data) {
		if (data) {
			//将article_info提升至全局，保证其他函数也可以调用。
			article_info = data;
		} else {
			alert('Error')
		}
	});

	//获取评论列表
	res.api.comment.get_list({
		"id": 5,
	}, function(error, data) {
		if (data) {
			console.log(data)
		} else {
			console.log(error)
		}
	});
	//发送评论
	$("#send_comment").click(function() {
		var comment = $("#myEditor").val();
		res.api.comment.post({
			"content": comment,
			"id": article_info.id,
		}, function(error, data) {
			if (data) {
				console.log(data);
			} else {
				console.log("Error")
			}
		});
	});
});