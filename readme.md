[TOC]
##KkBloG

KkBloG是一套基于Python的博客程序，采用Restful架构，简单易拓展，你可以轻松定制自己的博客界面。

这个项目是对[flask-restaction](https://github.com/guyskk/flask-restaction)框架的一次尝试，最初是准备做成个人博客，现在做成了一个公共博客系统，类似于[Readthedocs](https://readthedocs.org/)的模式。你可以用markdown格式写文章，保存到github，然后就可以在上面展示自己的博客，别人还可以评论你的文章。


我的博客 [http://www.kkblog.me](http://www.kkblog.me)

###安装

安装Python2.7和Python包管理器pip(貌似安装python时会自动安装上)

安装git

在命令行下执行

	python --version
	pip --version
	git --version

没有报错就OK了

下载kkblog
	
	git clone https://github.com/guyskk/kkblog.git

切换工作目录

	cd kkblog

安装kkblog

	pip install -r requires.txt

	or 

	python setup.py develop

启动

	python manage.py


###快速上手

[文档 http://127.0.0.1:5000/static/resdocs.html](http://127.0.0.1:5000/static/resdocs.html)

[res.js的用法](http://flask-restaction.readthedocs.org/zh/latest/quickstart.html#use-res-js)


打开[resdocs.html](http://127.0.0.1:5000/static/resdocs.html)页面，在控制台依次执行

	res.api.user.post_login({username:"admin@admin.com",password:"123456"})

	res.api.githooks.post_update({local:false,rebuild:true})

第一句是以管理员身份登录

第二句从github上下载我的文章，然后解析，之后就能看到文章了

没有报错就OK了，再执行

	res.api.article.get_list()

可以在Network里面看到返回结果

访问一下这些页面，没问题你就可以开始前端工作了

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

[http://127.0.0.1:5000/api/article/list](http://127.0.0.1:5000/api/article/list)

[http://127.0.0.1:5000/article/guyskk/article/微信页面整合WebApi](http://127.0.0.1:5000/article/guyskk/article/微信页面整合WebApi)

### 基本配置

配置文件在`kkblog/kkblog/config/`目录里面

- default_config.py 默认配置
- kkblog_config.cfg 部署到生产环境的配置
- permission.json 权限配置

default_config.py

	USER_ADMIN_EMAIL 管理员账号
	USER_ADMIN_PASSWORD 管理员密码
	USER_ADMIN_REPO_URL 管理员github博客仓库的url(要https开头的)

博客仓库
	
	/ 仓库根目录
	/subdir 子目录
	/subdir/article_xxx.md 文章
	/2015/python2编码问题.md 示例

对应的url

	/article/you_github_username/subdir/article_xxx
	/article/guyskk/2015/python2编码问题  --> 博客文章地址
	/article/guyskk  -->  article_list页面
	/login  -->  登录
	/register  -->  注册
	/          -->  首页

static目录
	
	article.html 文章内容
	article_list.html 文章列表
	login.html 登录
	register.html 注册
	index.html 首页

为了使搜索引擎能更好的收录文章，文章内容需要部分在服务端渲染，将以下标记插入到article.html中即可在服务端渲染 文章标题，目录，内容。可以看article.html源码中的用法。

	{{"article_title"}}
	{{"article_toc"}}
	{{"article_content"}}


----------------
**以下内容请暂时忽略**

Python2.7
	
	apt-get install python2.7

Python包管理器 pip <https://pip.pypa.io/en/latest/installing.html>

	sudo apt-get install python-pip

	//or

	wget https://bootstrap.pypa.io/get-pip.py
	python get-pip.py

	apt-get install libxml2-dev libxslt1-dev python-dev
	
用到的Python库

	pip install flask
	pip install flask-restaction
	pip install flask-cors
	pip install markdown
	pip install pony
	pip install pyquery
	pip install giturlparse.py
	pip install gittle

以后可能会用到的Python库

	pip install flask-restful
	pip install PyMongo
	pip install Flask-PyMongo
	pip install SQLAlchemy


数据库 mongodb 或者 mysql, 目前是sqlite
	
http://docs.mongodb.org/master/tutorial/install-mongodb-on-ubuntu/

	//mongodb及python客户端
	sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
	echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
	sudo apt-get update
	sudo apt-get install -y mongodb-org
	pip install pymongo
	
	//mysql及python客户端
	sudo apt-get install mysql-server 
	sudo apt-get install python-dev
	sudo apt-get install  libmysqld-dev
	pip install MySQL-python
	

服务器 nginx和uwsgi

	sudo apt-get install nginx
	sudo apt-get install python-dev
	pip install uwsgi


构建前端代码 Node.js和Grunt
	
	sudo apt-get install nodejs
	npm install -g grunt

Grunt插件

	jshint, uglify, concat,
	less, csslint, cssmin,
	lesslint, watch, qunit

前端css/js库
	
	//语法着色
	Linguist
	//前端css框架
	Bootstrap
	//js库
	jQuery.js
	//js库
	Angular.js

####配置Nginx和uwsgi

1. 配置Nginx

	```	
	cd /etc/nginx
	sudo vim nginx.conf
	//修改日志文件路径
	```

2. 修改start_nginx.sh

	```bash

	#!/bin/bash

	echo 更新代码
	wget ftp://192.168.56.1/ -r -X "oth","static/node_modules" -N -nv -P ..

	echo 复制nginx配置文件到/etc/nginx/sites-enabled
	sudo cp kkblog_nginx.conf /etc/nginx/sites-enabled

	echo 结束所有uwsgi进程
	killall -KILL uwsgi

	echo 启动uwsgi
	uwsgi --ini kkblog_uwsgi.ini

	echo 重启nginx
	sudo service nginx restart

	echo 查看uwsgi进程
	pgrep -a uwsgi

	echo 查看nginx进程
	pgrep -a nginx

	```

3. 启动

	```
	sudo chmod u+x start_nginx.sh
	./start_nginx.sh
	```

