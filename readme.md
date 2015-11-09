[TOC]
## KkBloG

KkBloG 是一套基于 Python 的博客程序，采用 Restful 架构，简单易拓展，你可以轻松定制自己的博客界面。

这个项目是对[flask-restaction](https://github.com/guyskk/flask-restaction)框架的一次尝试，最初是准备做成个人博客，现在做成了一个多人博客系统，类似于[Readthedocs](https://readthedocs.org/)的模式。你可以用 markdown 格式写文章，保存到 github ，然后就可以在上面展示自己的博客，别人还可以评论你的文章。


我的博客 [http://www.kkblog.me](http://www.kkblog.me)

###安装

安装 Python2.7 和 pip (貌似安装python的时候会自动装上)

安装 git

在命令行下执行

	python --version
	pip --version
	git --version

没有报错就OK了

下载 kkblog
	
	git clone https://github.com/guyskk/kkblog.git

切换工作目录

	cd kkblog

安装 kkblog

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

第二句从 github 上下载我的文章，然后解析，之后就能看到文章了

没有报错就OK了，再执行

	res.api.article.get_list()

可以在Network里面看到返回结果

访问一下这些页面，没问题你就可以开始前端工作了

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

[http://127.0.0.1:5000/api/article/list](http://127.0.0.1:5000/api/article/list)

[http://127.0.0.1:5000/article/guyskk/2015/微信页面整合WebApi](http://127.0.0.1:5000/article/guyskk/2015/微信页面整合WebApi)

注意：找回密码功能需要配置Mail账号密码

### 基本配置

#### 配置Mail账号密码（必须）

在 manage.py 文件同级目录下新建 kkblog_config.py，填写你的信息

	MAIL_SERVER = "例如smtp.qq.com"
	MAIL_USERNAME = "you_email@email.com"
	MAIL_DEFAULT_SENDER = "you_email@email.com"
	MAIL_PASSWORD = "you_email_password"

kkblog_config.py 文件是部署到生产环境的配置，修改后需要重启程序才能生效。


#### 其他配置文件在 `kkblog/kkblog/config/` 目录里面

- default_config.py 默认配置
- permission.json 权限配置

default_config.py

	USER_ADMIN_EMAIL 管理员账号
	USER_ADMIN_PASSWORD 管理员密码
	USER_ADMIN_REPO_URL 管理员github博客仓库的url(要https开头的)

#### 博客仓库
	
	/ 仓库根目录
	/subdir 子目录
	/subdir/article_xxx.md 文章
	/2015/python2编码问题.md 示例

对应的 url

	/article/you_github_username/subdir/article_xxx
	/article/guyskk/2015/python2编码问题  --> 博客文章地址
	/article/guyskk  -->  article_list页面
	/login  -->  登录
	/register  -->  注册
	/          -->  首页




### 部署到服务器

在 ubuntu v14.0 上测试通过
	
#### 服务器上安装 Nginx

	sudo apt-get install nginx

配置 Nginx

	sudo vim /etc/nginx/nginx.conf

	# 修改日志文件路径
	access_log /var/www/log/nginx_access.log;
    error_log /var/www/log/nginx_error.log;

	# 添加配置文件
    # include /etc/nginx/conf.d/*.conf;
    # include /etc/nginx/sites-enabled/*;
    include /var/www/config/nginx/*.conf;

#### 直接到服务器上部署

	cd /tmp
	git clone https://github.com/guyskk/kkblog.git
	cd kkblog
	
	# 新建 kkblog_config.py
	vim kkblog_config.py

	# 配置Mail账号密码
	# MAIL_SERVER = "例如smtp.qq.com"
	# MAIL_USERNAME = "you_email@email.com"
	# MAIL_DEFAULT_SENDER = "you_email@email.com"
	# MAIL_PASSWORD = "you_email_password"
	
	# 部署
	sudo bash deploy.sh

#### 或者远程部署

本地需要安装 python 2 和 fabric

	pip install fabric

获取代码

	git clone https://github.com/guyskk/kkblog.git

[配置Mail账号密码（必须）](#mail)

在 `fabfile.py` 同级目录下，新建 `fab_settings.py`，填写服务器信息
	
	hosts = [
	    "username@host_ip:port",
	    #例如"guyskk@127.0.0.1:22"
	]

部署

	fab deploy


#### 部署好之后会自动启动，默认端口是 5000

如果要手动启动或重启，在服务器上执行
	
	cd /var/www/kkblog
	sudo bash deploy.sh


### 前端

前端最好是用 angular.js 框架结合 res.js 来做

我只做了文章内容页面，用了定制的 bootstrap ，样式用的是 less 语法，使用 grunt 自动化构建。

static 目录
	
	article.html 文章内容
	article_list.html 文章列表
	login.html 登录
	register.html 注册
	index.html 首页

为了使搜索引擎能更好的收录文章，文章内容需要部分在服务端渲染，将以下标记插入到 article.html 中即可在服务端渲染 文章标题，目录，内容。可以看 article.html 源码中的用法。

	{{"article_title"}}
	{{"article_toc"}}
	{{"article_content"}}


构建前端代码 Node.js 和 Grunt
	
	sudo apt-get install nodejs
	npm install -g grunt

Grunt 插件

	jshint, uglify, concat,
	less, csslint, cssmin,
	lesslint, watch, qunit

前端 css/js 库
	
	//语法着色
	Linguist
	//前端css框架
	Bootstrap
	//js库
	jQuery.js
	//js库
	Angular.js

### 其他

用到的 Python 库

	pip install flask
	pip install pyjwt
	pip install flask-restaction
	pip install flask-cors
	pip install markdown
	pip install pony
	pip install pyquery
	pip install pygitutil
	pip install flask-mail
	pip install flask-cache

以后可能会用到的 Python 库

	pip install PyMongo
	pip install Flask-PyMongo
	pip install SQLAlchemy
	pip install snownlp
安装 git

	sudo apt-get install git

安装 python2.7

	sudo apt-get install python2.7

安装 python-dev

	sudo apt-get install python-dev

	
安装 pip

	sudo apt-get install python-pip
	or
	wget https://bootstrap.pypa.io/get-pip.py
	sudo python get-pip.py

安装 virtualenv

	sudo pip install virtualenv

安装 uwsgi

	sudo pip install uwsgi

安装 nginx

	sudo apt-get install nginx

安装 lxml

	# 用下面这两句不能通过 pip install lxml
	# sudo apt-get install libxml2-dev libxslt1-dev
	# sudo apt-get install python-lxml
	# 直接 pip install lxml 会报错
	# pip install pyquery -U 会重新安装 lxml, 也会导致报错

	# 正确方式
	sudo apt-get install build-essential libxml2-dev libxslt-dev lib32z1-dev python-dev
	sudo pip install lxml

安装 pillow

	apt-get install libjpeg-dev
	
数据库 mongodb 或者 mysql, 目前是 sqlite
	
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
	

服务器 nginx 和 uwsgi

	sudo apt-get install nginx
	sudo apt-get install python-dev
	sudo pip install uwsgi

	# centos
	# nginx
	# https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7
	#
	# pip
	# curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
	# python /tmp/get-pip.py
	# 

