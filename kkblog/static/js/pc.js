$(document).ready(function () {
	//个人中心的登录检测，同时把各项数据填写到合适的位置！
	res.api.userinfo.get_me(null,function (error,data) {
		if (data) {
			var photo_url = data.photo_url;
			var user_name = data.nickname;
			var user_phone = data.phone;
			var user_email = data.email;
			var user_id    = data.id;
			var user_date_create = data.date_create;
			
			$(".am-form input").eq(0).val(user_id);
			$(".am-form input").eq(1).val(user_email);
			$(".am-form input").eq(2).val(user_phone);
			$(".am-form input").eq(3).val(photo_url);
			
			if (photo_url==null) {
				$("#user_alert").removeClass("am-hide")
			}
			
			$("#user_photo").attr("src",photo_url);
			$(".user_name").html(user_name);
			$(".user_phone").html(user_phone);
			$(".user_email").html(user_email);
			$(".user_id").html(user_id);
			$(".user_date_create").html(user_date_create);
		} else{
			alert("帐号未登录！")
		}		
	})
	//修改页面保存个人信息
	$("#user_saveinfo").click(function () {
		var nickname = $(".am-form input").eq(0).val();
		var email = $(".am-form input").eq(1).val();
		var phone = $(".am-form input").eq(2).val();
		var photo_url = $(".am-form input").eq(3).val();
		console.log(photo_url)
		res.api.userinfo.put(
			{
				"nickname": nickname,
				"email": email,
				"phone": phone,
				"photo_url": photo_url
			},
			function (error,data) {
				if (data) {
					alert("修改成功");
					$("#user_changeInfo").addClass("am-hide");
					$("#user_showInfo").removeClass("am-hide");
					location.href="/static/personal_center.html";
				} else {
					alert("修改失败，请稍后尝试！")
				}
			}
		
		)
	});
	//开始完善信息。
	$("#user_completeMessage").click(function (e) {
		e.preventDefault();
		$("#user_alert").addClass("am-hide");
		$("#user_showInfo").addClass("am-hide");
		$("#user_changeInfo").removeClass("am-hide");
	});
	//进入修改用户信息界面。
	$("#user_change").click(function () {
		$("#user_showInfo").addClass("am-hide");
		$("#user_changeInfo").removeClass("am-hide");
	});
	//退出修改用户信息界面
	$("#user_cancelChange").click(function () {
		$("#user_changeInfo").addClass("am-hide");
		$("#user_showInfo").removeClass("am-hide");
	});
	
	//github地址弹出框
	$("#user_pcblog").on("click",function () {
		$("#user_gitUrl").modal({
			relatedTarget:this,
			onConfirm:function (e) {
				var article_repo = $("#user_gitUrl input").eq(0).val();
				console.log(article_repo)
				res.api.bloguser.post(
					{
						"article_repo":article_repo,
					},
					function (error,data) {
						if (data) {
							alert("已成功添加")
						} else{
							alert("ERROR")
							console.log(error)
						}
					}
				)
			},
			onCancel:function (e) {}
		})
	});
	
	//当检测到已登录且github仓库已开启，则自动显示更新文章的按钮。
	res.api.bloguser.get_me(null,function (error,data) {
		if (data) {
			$("#user_pcblog").addClass("am-hide");
			$("#user_blog_update").removeClass("am-hide");
			$("#user_watch").removeClass("am-hide");
			//保存gituser的名字，用于查看个人文章。
			localStorage.setItem('git_username',data.git_username);
		}
	});
	//更新文章。
	$("#user_blog_update").click(function () {
		$("#user_blog_update").addClass("am-disabled");
		res.api.githooks.post_update(
			{
				local:false,rebuild:true
			},function (error,data) {
				if (data) {
					alert("更新成功");
					$("#user_blog_update").removeClass("am-disabled");
				} else {
					alert("出错！");
					console.log(error);
					$("#user_blog_update").removeClass("am-disabled");
				}
			}
		);
	});
	
	$("#user_watch").click(function () {
		location.href = '/static/pc_article.html'
	})
})
