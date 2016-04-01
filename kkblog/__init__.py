# coding:utf-8
"""
注册用户并设置博客仓库地址:
    res.user.post_signup({userid:'guyskk',password:'123456'})
    res.user.post_login({userid:'guyskk',password:'123456'})
    res.user.put({repo: 'https://github.com/guyskk/kkblog-article.git'})
同步博客仓库:
    res.user.post_sync_repo({})
"""
from __future__ import unicode_literals, absolute_import, print_function
import os
from flask import Flask, Blueprint
from werkzeug.local import LocalProxy
from flask_restaction import Api, Gen, Auth, Permission
from flask_github import GitHub
from .flask_couchdb import CouchDB

couch = CouchDB()
db = LocalProxy(lambda: couch.db)
github = GitHub()
api = Api(docs=__doc__)
auth = Auth()

from .webhooks import Webhooks
from .user import User
from .article import Article
from .comment import Comment
from .captcha import Captcha


def fn_user_role(token):
    if token and "userid" in token:
        user = db.get(token["userid"], None)
        if user is not None:
            return user["role"]
    return None


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object("kkblog.config_default")
    if config:
        app.config.from_object(config)

    app.route("/webhooks")(Webhooks())
    route_views(app)
    couch.init_app(app)
    github.init_app(app)

    bp_api = Blueprint('api', __name__, static_folder='static')
    api.init_app(app, blueprint=bp_api)
    api.add_resource(Article)
    api.add_resource(Comment)
    api.add_resource(User)
    api.add_resource(Captcha)
    api.add_resource(Permission, auth=auth)
    auth.init_api(api, fn_user_role=fn_user_role)
    app.register_blueprint(bp_api, url_prefix='/api')

    gen = Gen(api)
    gen.resjs()
    gen.resdocs()
    gen.permission()
    return app


def route_views(app):
    views = [
        ("/", "index.html"),
        ("/login", "login.html"),
        ("/signup", "signup.html"),
        ("/<userid>", "article-user.html"),
        ("/<userid>/<catalog>", "article-catalog.html"),
        ("/<userid>/<catalog>/<article>", "article.html"),
    ]

    # 静态文件
    def make_view(filename):
        return lambda *args, **kwargs: app.send_static_file(filename)

    for url, filename in views:
        end = os.path.splitext(filename)[0]
        app.route(url, endpoint=end)(make_view(filename))


def config_cors(app):
    # 跨域
    from flask_cors import CORS
    auth_header = app.config.get("API_AUTH_HEADER") \
        or getattr(api, "auth_header")
    resources = {
        r"*": {"expose_headers": [auth_header]},
    }
    CORS(app, resources=resources)
