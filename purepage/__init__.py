"""PurePage

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
"""
import os
from flask import Flask, Blueprint, abort, g
from werkzeug.routing import BaseConverter, ValidationError
from flask_restaction import Resource, Gen, Permission
from couchdb.http import NotFound
from purepage.exts import db, github, mail, limiter, api, auth
from purepage.webhooks import Webhooks
from purepage.views.user import User
from purepage.views.article import Article
from purepage.views.comment import Comment
from purepage.views.captcha import Captcha


class Info(Resource):

    def get(self):
        return "welcome to purepage!"

    def get_404(self):
        abort(404, 'test')

    def get_403(self):
        abort(403, 'test')

    def get_400(self):
        abort(400, 'test')

    def get_500(self):
        raise ValueError('test')

resources = [Info, User, Article, Comment, Captcha]


def fn_user_role(token):
    if token and "userid" in token:
        try:
            user = db.get(token["userid"])
            g.user = user
            g.userid = token["userid"]
            return user["role"]
        except NotFound:
            pass
    g.user = None
    g.userid = None
    return None


class NoConverter(BaseConverter):
    """NoConverter."""

    def __init__(self, map, *items):
        BaseConverter.__init__(self, map)
        self.items = items

    def to_python(self, value):
        if value in self.items:
            raise ValidationError()
        return value


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object("purepage.config_default")
    if config:
        app.config.from_object(config)
    app.url_map.converters['no'] = NoConverter
    app.route("/webhooks")(Webhooks())
    route_views(app)
    db.init_app(app)
    github.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    bp_api = Blueprint('api', __name__, static_folder='static')
    api.init_app(app, blueprint=bp_api, docs=__doc__)
    for x in resources:
        api.add_resource(x)
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
        ("/<no(static):userid>", "user.html"),
        ("/<no(static):userid>/<catalog>", "catalog.html"),
        ("/<no(static):userid>/<catalog>/<article>", "article.html"),
    ]

    # 静态文件
    def make_view(filename):
        return lambda *args, **kwargs: app.send_static_file(filename)

    for url, filename in views:
        endpoint = os.path.splitext(filename)[0]
        app.route(url, endpoint=endpoint)(make_view(filename))


def config_cors(app):
    # 跨域
    from flask_cors import CORS
    auth_header = app.config.get("API_AUTH_HEADER") \
        or getattr(api, "auth_header")
    resources = {
        r"*": {"expose_headers": [auth_header]},
    }
    CORS(app, resources=resources)
