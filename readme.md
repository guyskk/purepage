## KkBloG

**注意，此项目正在重写！**


KkBloG 是一套基于 Python 的博客程序，采用 Restful 架构，简单易拓展，你可以轻松定制自己的博客界面。

这个项目是对[flask-restaction](https://github.com/guyskk/flask-restaction)框架的一次尝试，最初是准备做成个人博客，现在做成了一个多人博客系统，类似于[Read the docs](https://readthedocs.org/)的模式。


###安装

#### Windows 

1. 安装 Git
2. 安装 Python 2.7 最新版，用 Python3 有些依赖的库安装很麻烦

	在命令行下执行

		python --version
		pip --version
		git --version

	没有报错就 OK 了

4. 安装 CouchDB

	下载&安装即可
	http://couchdb.apache.org/

3. 安装 kkblog
	
		git clone https://github.com/guyskk/kkblog.git
		cd kkblog
		pip install -e .

4. 初始化数据库&启动
		
		python manage.py initdb
		python manage.py runserver -dr

	访问 http://127.0.0.1:5000/static/resdocs.html 查看 API 文档

	打开浏览器控制台，注册用户并设置博客仓库地址:

		res.user.post_signup({userid:'guyskk',password:'123456'})
		res.user.post_login({userid:'guyskk',password:'123456'})
		res.user.put({repo: 'https://github.com/guyskk/kkblog-article.git'})
	
	
### 快速上手


#### 基本配置

在 manage.py 文件同级目录下新建 config_product.py，填写配置信息

配置Mail账号密码（找回密码功能需要配置Mail账号密码）

	MAIL_SERVER = "例如smtp.qq.com"
	MAIL_USERNAME = "you_email@email.com"
	MAIL_DEFAULT_SENDER = "you_email@email.com"
	MAIL_PASSWORD = "you_email_password"

设置管理员账号（默认账号admin，密码123456）

	USER_ADMIN_EMAIL 管理员账号
	USER_ADMIN_PASSWORD 管理员密码
	USER_ADMIN_REPO_URL 管理员github博客仓库地址


博客仓库
	
	/ 仓库根目录
	/catalog 子目录
	/catalog/article_xxx.md 文章
	/2015/python2编码问题.md 示例

#### 路由
	
路径                | 对应的html           | 内容
------------------- | -------------------- | --------------------------
/                   | index.html           | 首页，主要显示最新文章列表
/login              | login.html           | 登录
/signup             | signup.html          | 注册
/userid             | article-user.html    | 显示具体用户的最新文章列表
/userid/catalog     | article-catalog.html | 显示具体用户的文章归档
/userid/catalog/xxx | article.html         | 显示具体文章


### 前端

使用 res.js 可以方便的调用 api。  
[res.js的用法](http://flask-restaction.readthedocs.org/zh/latest/quickstart.html#res-js)


为了使搜索引擎能更好的收录文章，文章内容需要部分在服务端渲染，将以下标记插入到 article.html 中即可在服务端渲染 文章标题，内容。

	{{"article_title"}}
	{{"article_content"}}


### 其他

安装 python-dev

	apt-get install python-dev

安装 pip

	apt-get install python-pip

安装 uwsgi

	pip install uwsgi

安装 lxml

	# 用下面这两句不能通过 pip install lxml
	# apt-get install libxml2-dev libxslt1-dev
	# apt-get install python-lxml
	# 直接 pip install lxml 会报错
	# pip install pyquery -U 会重新安装 lxml, 也会导致报错

	# 正确方式
	apt-get install build-essential libxml2-dev libxslt-dev lib32z1-dev python-dev
	pip install lxml

安装 pillow

	apt-get install libjpeg-dev
	
