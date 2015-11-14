# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

from flask import Flask, Blueprint, abort, current_app
from pony.orm import sql_debug, db_session
import re
import os
from datetime import datetime
from validater import add_validater, validaters
import logging
from logging.handlers import RotatingFileHandler

from kkblog.extensions import api, db, cache, mail
from kkblog import (model, user, bloguser, userinfo, article,
                    tag, comment, githooks, captcha)

# __all__ must be str, can't be unicode
__all__ = [str("create_app"), str("api"), str("db")]


def user_role(uid, user):
    user_model = {
        "user": (model.User, "id"),
        "bloguser": (model.BlogUser, "user_id"),
    }
    with db_session:
        User, key = user_model[user]
        u = User.get(**{key: uid})
        if u:
            return u.role


def create_app():
    app = Flask(__name__)
    config_app(app)
    config_logging(app)

    bp_api = Blueprint('api', __name__, static_folder='static')
    api.init_app(bp_api, fn_user_role=user_role)
    api.config(app.config)
    if app.config.get("ALLOW_CORS"):
        config_cors(app)

    cache.init_app(app)
    mail.init_app(app)

    config_validater(app)
    config_view(app)
    config_api(app)
    config_db(app)
    config_error_handler(app)
    config_before_handler(app)
    config_after_handler(app)

    app.register_blueprint(bp_api, url_prefix='/api')

    return app


def config_cors(app):
    # 跨域
    from flask.ext.cors import CORS
    auth_header = app.config.get("API_AUTH_HEADER") or api.auth_header
    resources = {
        r"*": {"expose_headers": [auth_header]},
    }
    CORS(app, resources=resources)


def config_app(app):

    app.config.from_object('kkblog.config.default_config')
    app.config.from_envvar('KKBLOG_CONFIG', silent=True)

    # create dir_data and dir_article
    dir_article = app.config["ARTICLE_DEST"]
    if not os.path.isabs(dir_article):
        dir_article = os.path.join(app.root_path, dir_article)
        app.config["ARTICLE_DEST"] = dir_article
    if not os.path.exists(dir_article):
        os.makedirs(dir_article)
    # 图形验证码字体文件
    app.config["CAPTCHA_FONT"] = os.path.join(
        app.root_path, app.config["CAPTCHA_FONT"])
    app.config["flask_profiler"] = {
        "enabled": app.config["DEBUG"],
        "storage": {
            "engine": "sqlite"
        }
    }


def config_validater(app):

    def friendly_date(date):
        s = "{}年{}月{}日".format(date.year, date.month, date.day)
        return s

    def iso_datetime_validater(v):
        """iso_str -> datetime or datetime -> iso_str"""
        if isinstance(v, datetime):
            return (True, v.isoformat())
        else:
            return validaters["datetime"](v)

    def friendly_date_validater(v):
        if isinstance(v, datetime):
            return (True, friendly_date(v))
        else:
            return (False, None)
    add_validater("iso_datetime", iso_datetime_validater)
    add_validater("friendly_date", friendly_date_validater)


def config_view(app):

    pattern_article_path = re.compile(r"(.*)/(.*)/(.*)")

    def render_mark(text, **kwargs):
        """将标记替换成具体内容"""
        for k, v in kwargs.items():
            mark = '{{"%s"}}' % k
            text = text.replace(mark, v)
        return text

    # article 页面需要服务端部分渲染
    @app.route('/article/<path:path>')
    def page_article(path):
        p = pattern_article_path.findall(path)
        if not p:
            abort(404)
        gitname, subdir, name = p[0]
        with app.open_resource("static/article.html") as f:
            art = article.get_article(gitname, subdir, "%s.md" % name)
            if not art:
                abort(404)
            title = art["title"]
            cont = art["content"]["html"]
            toc = art["content"]["toc"]
            contents = f.read().decode("utf-8")
            contents = render_mark(contents, article_title=title,
                                   article_content=cont, article_toc=toc)
            return contents

    view_urls = (
        ("article_list.html", '/article/<gitname>'),
        # ("register.html", '/register'),
        # ("login.html", '/login'),
        ("reset_password.html", "/reset_password"),
        ("index.html", '/'),
        ("favicon.ico", '/favicon.ico'),
    )

    # 转发 static 文件
    def make_view(fname):
        return lambda *args, **kwargs: app.send_static_file(fname)

    for filename, url in view_urls:
        end = os.path.splitext(filename)[0]
        app.route(url, endpoint=end)(make_view(filename))


def config_api(app):
    reslist = [
        article.Article,
        tag.Tag,
        githooks.GitHooks,
        user.User,
        bloguser.BlogUser,
        comment.Comment,
        userinfo.UserInfo,
        captcha.Captcha,
    ]
    for res in reslist:
        api.add_resource(res)


def config_error_handler(app):

    @app.errorhandler(404)
    def page_not_found(e):
        return app.send_static_file('404.html'), 404


def config_db(app):
    # 让sqlite数据库文件位置相对于应用程序根目录
    params = app.config["DATABASE_PARAMS"]
    if "filename" in params and not os.path.isabs(params["filename"]):
        params["filename"] = os.path.join(app.root_path, params["filename"])
    db_dir = os.path.dirname(params["filename"])
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # 测试时会多次执行db.bind
    try:
        db.bind(app.config["DATABASE_NAME"], create_db=True, **params)
        db.generate_mapping(create_tables=True)
    except TypeError as ex:
        app.logger.warn("can't bind db: " + str(ex))
    # 多次执行 create_tables 不会报错
    db.create_tables()


def config_before_handler(app):

    @app.before_first_request
    def init():
        api.gen_resjs()
        api.gen_resdocs()
        email = current_app.config["USER_ADMIN_EMAIL"]
        password = current_app.config["USER_ADMIN_PASSWORD"]
        repo = current_app.config["USER_ADMIN_REPO_URL"]
        # 添加管理员
        user.add_admin(email, password)
        with db_session:
            u = model.User.get(username=email)
            bloguser.add_admin(u.id, repo)

    @app.after_request
    def after_request(resp):
        return resp


def config_after_handler(app):
    pass


def config_logging(app):
    # pony_orm debug 信息
    if app.config.get("SQL_DEBUG"):
        sql_debug(True)
    # 设置 debug_level
    if app.config.get("DEBUG_LEVEL"):
        level = getattr(logging, app.config.get("DEBUG_LEVEL"))
        logging.basicConfig(level=level)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    debug_log = os.path.join(app.root_path, app.config['DEBUG_LOG'])
    debug_file_handler = RotatingFileHandler(debug_log, maxBytes=100000,
                                             backupCount=10)
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path, app.config['ERROR_LOG'])
    error_file_handler = RotatingFileHandler(error_log, maxBytes=100000,
                                             backupCount=10)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)
