$(document).ready(function() {
	/*
	 先传入header和footer，保证页面视图优先加载。
	 之后加载popUp弹出页面，同时把函数放置在内。
	 因为当一个作用域内有function，则function在被编译时会提到头部。
	 如果放在别的ajax函数之前，则会出现找不到页面dom元素，从而函数失效。
	 所以这些操作页面元素的函数应该等页面加载（ajax）完成后再进行加载。
	 */

	//获取页面顶部导航
	$.ajax({
		type: "get",
		url: "/static/header.html",
		async: true,
		success: function(header) {
			$("header").append(header);
			//根据页面中#header的data-name属性，从而把相应的class："am-active"加上
			var div_data = $("header").data("name")
			switch(div_data) {
				case "home":
					$("#nav_homepage").addClass("am-active");
					break;
				case "article":
					$("#nav_article a").removeClass("am-hide");
					$("#nav_article").addClass("am-active");
					break;
				case "pc":
					$("#nav_pc").addClass("am-active")
				default:
					break;
			}
		},
		error: function(e) {
			alert("Ajax失败，请检查文件是否存在或者是否设置为post！");
			console.log(e.responseText);
		}
	});
	//获取页面底栏
	$.ajax({
		type: "get",
		url: "/static/footer.html",
		async: true,
		success: function(footer) {
			$("footer").append(footer);
		},
		error: function(e) {
			alert("Ajax失败，请检查文件是否存在或者是否设置为post！");
			console.log(e.responseText);
		}
	});
	//获取页面弹出框部分，这一步后所有页面元素已经加载完毕。
	//然后开始加载函数，对dom进行操作。
	$.ajax({
		type: "get",
		url: "/static/popUp.html",
		async: true,
		success: function(popUp) {
			$("#popUp").append(popUp);
			//Ajax传入footer部分
			//给注册部分重合的代码加上div.
			$(".register div").addClass("am-input-group am-input-group-secondary am-u-sm-centered");
			//开始检测一次，确保登录状态能正确显示。
			islogin();
			//检测用户是否登录,当有token信息存在时则显示个人中心和登出选项。
			function islogin() {
				res.api.userinfo.get_me(null, function(error, data) {
					if (data) {
						console.log(data)
						pc_show();
					} else {
						pc_hide();
					}
				})
			};
			//打开遮罩

			function mask_open() {
				var height = $(window).height();
				$("#mask").css("height", height);
				$("#mask").css("visibility", "visible");
			};
			//关闭遮罩

			function mask_close() {
				$("#mask").css("height", "100%");
				$("#mask").css("visibility", "hidden");
			};
			//显示弹出框，传入两个参数作为指定的元素和弹出的高度

			function popUp_open(id, popup_height) {
				mask_open();
				$(id).css("visibility", "visible");
				$(id).animate({
					height: popup_height,
				});
			};
			//关闭弹出框，传入元素类或id即可关闭

			function popUp_close(id) {
				$(id).css("visibility", "hidden");
				mask_close();
			};


			//弹出个人中心和登出选项
			function pc_show() {
				$("#login,#register").addClass("am-hide");
				$("#pc,#log_out").removeClass("am-hide");
			};
			//隐藏个人中心和登出选项

			function pc_hide() {
				$("#pc,#log_out").addClass("am-hide");
				$("#login,#register").removeClass("am-hide");
			};

			//弹出登录页面
			$("#login").click(function(e) {
				e.preventDefault();
				popUp_open(".login", "300px");
			});
			//关闭登录页面
			$("#close_login").click(function() {
				popUp_close(".login");
			});

			//弹出注册页面
			$("#register").click(function(e) {
				e.preventDefault();
				popUp_open(".register", "370px");
			});
			//注册页面到登录页面
			$("#register_To_login").click(function() {
				popUp_close(".register");
				popUp_open(".login", "300px");
			});
			//关闭注册页面
			$("#close_register").click(function() {
				popUp_close(".register");
			});


			//用户登录
			$("#login-button").click(function() {
				var username = $(".login input").eq(0).val();
				var password = $(".login input").eq(1).val();
				res.api.user.post_login({
						"username": username,
						"password": password,
					},
					function(error, data) {
						islogin();
						if (error) {
							console.log('Error');
							alert("登录失败！Token信息获取失败。请确认用户名和密码。")
						}
						console.log(data);
						alert(data.username + "登陆成功！")
							//保存这些数据是为了个人中心的调用，和全网页别的部分的调用。
						popUp_close(".login");
					}
				)
			});
			//用户注册
			$("#register_button").click(function() {
				var email = $(".register input").eq(0).val();
				var password = $(".register input").eq(1).val();
				var password_check = $(".register input").eq(2).val();
				console.log(password + "  " + password_check)
				if (password == password_check) {
					$.ajax({
						type: "post",
						url: "/api/user/register",
						data: JSON.stringify({
							"email": email,
							"password": password,
						}),
						contentType: "application/json",
						success: function(data) {
							alert("注册成功!您的ID是" + data.id + "，用户名是:" + data.username);
							popUp_close(".register");
						}
					});
				} else {
					alert("两次输入密码不一致")
				}
			});
			//打开找回密码的弹出框
			$("#forget_password").click(function() {
				popUp_close(".login");
				popUp_open(".forgetPassword", "200px");
			});
			//提交找回密码的申请
			$("#button_forgetPassword").click(function() {
				var username = $(".forgetPassword input").eq(0).val();
				//button_forgetPassword点击发送，禁用按钮
				$("#button_forgetPassword").addClass("am-disabled")
				$.ajax({
					type: "post",
					url: "/api/user/forgot_password",
					data: JSON.stringify({
						"username": username,
					}),
					contentType: "application/json",
					success: function(data) {
						alert(data.message);
						$("#button_forgetPassword").removeClass("am-disabled");
					},
					error: function(e) {
						alert("出现错误，请重试！" + e.responseText)
						$("#button_forgetPassword").removeClass("am-disabled");
					}
				});
			});

			//关闭找回密码的弹出框
			$("#close_forgetPassword").click(function() {
				popUp_close(".forgetPassword");
			});

			//重新设置密码
			$("#reset_button").click(function() {
				var password = $(".article_title input").eq(0).val();
				var password_check = $(".article_title input").eq(1).val();
				var url = window.location.href;
				//《javascript高级程序设计》 P107，正则表达式
				var reg = /\be.*/gi;
				//exec函数返回一个数组，数组的第一位是正则表达式的结果
				var reset_token = reg.exec(url)[0]
				console.log(reset_token);

				if (password == password_check) {
					$.ajax({
						type: "post",
						url: "/api/user/reset_password",
						data: JSON.stringify({
							"password": password,
							"token": reset_token,
						}),
						contentType: "application/json",
						success: function() {
							alert("修改成功！");
						},
						error: function(e) {
							alert("修改失败，请重新尝试。错误信息：" + e.responseText);
						}
					});
				} else {
					alert("两次输入不一致")
				}
			});

			//登出
			$("#log_out").click(function(e) {
				e.preventDefault();
				alert("登出成功！");
				localStorage.clear();
				location.href = "/";
			});

			/*网页Ajax主体部分*/
		},
		error: function(e) {
			alert("Ajax失败，请检查文件是否存在或者是否设置为post！")
			console.log(e.responseText);
		}
	});

})