"""
# PurePage

注册

    res.user.post_signup({username:'guyskk',password:'123456'})

登录

    res.user.post_login({username:'guyskk',password:'123456'})

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


ALL_TABLE = ["user", "article"]
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
    else:
        app.config.from_envvar("PUREPAGE_CONFIG", silent=True)

    init_github(app)
    init_mail(app)
    init_limiter(key_func=get_remote_address)
    init_db(app, tables=ALL_TABLE)
    config_api(app)
    return app


def config_api(app):
    api = Api(app, metafile="meta.json", docs=__doc__)
    app.route("/")(api.meta_view)
    auth = init_auth(api)
    auth.get_role(get_role)
    for x in ALL_RESOURCE:
        api.add_resource(x)
