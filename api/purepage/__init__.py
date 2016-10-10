"""
## PurePage

注册用户并设置博客仓库:
1. 验证邮箱
res.user.post_verify({userid:'guyskk',email:'guyskk@qq.com'})
2. 在(命令行)控制台里面会显示发送的邮件内容，取出其中的token
3. 注册
res.user.post_signup({token:token,password:'123456'})
4. 登录
res.user.post_login({userid:'guyskk',password:'123456'})
5. 设置代码仓库
res.user.put({repo: 'https://github.com/guyskk/purepage-article.git'})
6. 同步博客仓库:
res.user.post_sync_repo({})


$shared:
    message:
        message?str: 提示信息
    pagging:
        page?int&min=1&default=1: 第几页
        per_page?int&min=1&max=100&default=10: 每页数量
"""
from flask import Flask, g
from flask_restaction import Api
from flask_limiter.util import get_remote_address
from .ext import (
    r, db, init_db, init_github, init_mail, init_limiter, init_auth
)
from . import views


ALL_RESOURCE = [getattr(views, x) for x in dir(views) if x[:1].isupper()]


def get_role(token):
    if token and token.get("type") == "login":
        g.user = user = db.run(r.table("user").get(token["id"]))
        if user:
            return user["role"]
    return "guest"


def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object("purepage.config")
    if config:
        app.config.from_object(config)

    init_github(app)
    init_mail(app)
    init_limiter(key_func=get_remote_address)
    init_db(app)
    config_api(app)
    return app


def config_api(app):
    api = Api(app, metafile="meta.json", docs=__doc__)
    app.route("/")(api.meta_view)
    auth = init_auth(api)
    auth.get_role(get_role)
    for x in ALL_RESOURCE:
        api.add_resource(x)
