[TOC]
##KkBloG

KkBloG是一套基于Python的个人博客程序，采用Restful架构，简单易用，高性能，易拓展，你可以轻松定制自己的博客界面。

我的博客 <http://www.kkblog.me>

###安装相关依赖

Python2.7
	
	apt-get install python2.7

Python包管理器 pip <https://pip.pypa.io/en/latest/installing.html>

	sudo apt-get install python-pip

	//or

	wget https://bootstrap.pypa.io/get-pip.py
	python get-pip.py


用到的Python库

	pip install flask
	pip install flask-restaction
	pip install flask-cors
	pip install markdown
	pip install pony
	pip install pyquery

###快速上手

文档
http://127.0.0.1:5000/static/resdocs.html

res.js的用法，调用api要用到
http://flask-restaction.readthedocs.org/zh/latest/quickstart.html#use-res-js

启动

	python run.py


然后访问 http://127.0.0.1:5000/api/githooks ，他会从github上下载我的文章，然后解析，之后就能看到文章了

访问一下这些页面，没问题你就可以开工了
http://127.0.0.1:5000/
http://127.0.0.1:5000/api/article/list
http://127.0.0.1:5000/article/微信页面整合WebApi


----------------
**以下内容请暂时忽略**

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

