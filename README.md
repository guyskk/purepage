## PurePage

PurePage 是基于 Python 的博客程序，类似于 [Read the docs](https://readthedocs.org/) 的模式。

这个项目是对 [flask-restaction](https://github.com/guyskk/flask-restaction) 框架的一次尝试。

PurePage 致力于达到以下目标:

1. 良好的写作体验和阅读体验
2. 易于分享和发现有价值的文章
3. 运行稳定，安全，快速
4. 开放API

### 部署

PurePage使用docker-compose进行部署。

安装完docker和docker-compose之后，执行以下命令:

    git clone https://github.com/guyskk/purepage.git
    cd purepage
    docker-compose up -d
    docker-compose exec api python manage.py db --create --root

访问RethinkDB管理界面:

    # 开启ssh代理
    ssh -L 8080:localhost:8080 user@server
    # 本地访问localhost:8080

### 技术栈

前端: Vue.js + Material Design Lite  
后端: Flask-Restaction + RethinkDB + Docker  
