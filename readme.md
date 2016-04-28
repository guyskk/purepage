## PurePage

**此项目正在重写！**

PurePage 是基于 Python 的博客程序，类似于 [Read the docs](https://readthedocs.org/) 的模式。

这个项目是对 [flask-restaction](https://github.com/guyskk/flask-restaction) 框架的一次尝试。

PurePage 致力于达到以下目标:

1. 良好的写作体验和阅读体验
2. 易于分享和发现有价值的文章
3. 运行稳定，安全，快速
4. 开放API

### 安装

PurePage 使用 docker 进行部署，linux 平台下需要安装 docker 和 docker-compose，
windows 和 mac 需要安装 docker-toolbox。安装教程请参考 https://docs.docker.com/ 。

安装完docker之后，执行以下命令:
```
git clone https://github.com/guyskk/purepage.git
cd purepage
docker-compose up
```

稍等片刻，PurePage 启动成功之后， 
访问 http://127.0.0.1:5000/static/resdocs.html 查看 API 文档

打开浏览器控制台，注册用户并设置博客仓库地址:

    res.user.post_signup({userid:'guyskk',password:'123456'})
    res.user.post_login({userid:'guyskk',password:'123456'})
    res.user.put({repo: 'https://github.com/guyskk/kkblog-article.git'})

最后，同步博客仓库:

    res.user.post_sync_repo({})
	

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
	
路径                    | 对应的html        | 内容
----------------------- | ----------------- | --------------------------
/                       | index.html        | 首页，主要显示最新文章列表
/login                  | login.html        | 登录
/signup                 | signup.html       | 注册
/userid                 | user.html         | 显示具体用户的最新文章列表
/userid/catalog         | catalog.html      | 显示具体用户的文章归档
/userid/catalog/article | article.html      | 显示具体文章


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
	
