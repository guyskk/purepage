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
from flask import Flask
from flask import Blueprint
from werkzeug.routing import BaseConverter, ValidationError
from flask_restaction import Api
from .dependency import d, github, mail, limiter
from .util import render_template
from purepage.webhooks import Webhooks
# from purepage.views.user import User
# from purepage.views.article import Article
# from purepage.views.comment import Comment
# from purepage.views.captcha import Captcha


# resources = [User, Article, Comment, Captcha]


# def fn_user_role(token):
#     if token and "userid" in token:
#         try:
#             user = db.get(token["userid"])
#             g.user = user
#             g.userid = token["userid"]
#             return user["role"]
#         except NotFound:
#             pass
#     g.user = None
#     g.userid = None
#     return None

RESERVED_WORDS = ['api', 'webhooks', 'docs', 'login', 'signup']


class NotReservedConverter(BaseConverter):
    """NotReservedConverter"""

    def to_python(self, value):
        if value in RESERVED_WORDS:
            raise ValidationError()
        return value


def create_app(config=None):
    app = Flask(__name__)
    # app.debug = True
    app.config.from_object("purepage.config_default")
    # if config:
    #     app.config.from_object(config)
    app.url_map.converters['not_reserved'] = NotReservedConverter
    app.route("/webhooks")(Webhooks())
    config_route(app)
    github.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    bp_api = Blueprint('api', __name__)
    d.api = api = Api(bp_api, docs=__doc__)

    # app.add_url_rule("/docs", view_func=api.meta_view)
    api.add_resource(type('Docs', (), {'get': api.meta_view}))
    # for x in resources:
    #     api.add_resource(x)
    app.register_blueprint(bp_api, url_prefix='/api')
    return app


def config_route(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/<not_reserved:userid>')
    def user(userid):
        return render_template('user.html')

    @app.route('/<not_reserved:userid>/<catalog>')
    def catalog(userid, catalog):
        return render_template('catalog.html')

    @app.route('/<not_reserved:userid>/<catalog>/<article>')
    def article(userid, catalog, article):
        return render_template('article.html')
