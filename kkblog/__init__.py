# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

from flask import Flask, Blueprint, abort, current_app
from pony.orm import sql_debug, db_session
import re
import os
from datetime import datetime
from validater import add_validater
import logging
from logging.handlers import RotatingFileHandler

from kkblog.extensions import api, db, cache, mail
from kkblog import model, user, bloguser, userinfo, article, comment, githooks

# __all__ must be str, can't be unicode
__all__ = [str("create_app"), str("api"), str("db")]


def create_app():
    app = Flask(__name__)
    config_app(app)
    config_logging(app)

    bp_api = Blueprint('api', __name__, static_folder='static')
    api.init_app(bp_api)
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
        r"*": {},
        r"/api/user/login": {
            "expose_headers": [auth_header],
        },
        r"/api/user/logout": {
            "expose_headers": [auth_header],
        }
    }
    CORS(app, resources=resources)


def config_app(app):

    app.config.from_object('kkblog.config.default_config')
    app.config.from_envvar('KKBLOG_CONFIG', silent=True)

    # create dir_article
    dir_article = app.config["ARTICLE_DEST"]
    if not os.path.isabs(dir_article):
        dir_article = os.path.join(app.root_path, dir_article)
    if not os.path.exists(dir_article):
        os.makedirs(dir_article)


def config_validater(app):

    def friendly_date(date):
        s = "{}年{}月{}日".format(date.year, date.month, date.day)
        return s

    def iso_datetime_validater(v):
        if isinstance(v, datetime):
            return (True, v.isoformat())
        else:
            return (False, None)

    def friendly_date_validater(v):
        if isinstance(v, datetime):
            return (True, friendly_date(v))
        else:
            return (False, None)
    add_validater("iso_datetime", iso_datetime_validater)
    add_validater("friendly_date", friendly_date_validater)

    user_roles = ["user.admin", "user.normal"]

    def userrole_validater(v):
        return (True, v) if v in user_roles else (False, None)
    add_validater("userrole", userrole_validater)

    bloguser_roles = ["bloguser.admin", "bloguser.normal"]

    def bloguser_role_validater(v):
        return (True, v) if v in bloguser_roles else (False, None)
    add_validater("bloguser_role", bloguser_role_validater)


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
        git_username, subdir, name = p[0]
        with app.open_resource("static/article.html") as f:
            art = article.get_article(git_username, subdir, "%s.md" % name)
            if not art:
                abort(404)
            title, cont, toc = art["meta"]["title"], art["content"], art["toc"]
            contents = f.read().decode("utf-8")
            contents = render_mark(contents, article_title=title,
                                   article_content=cont, article_toc=toc)
            return contents

    view_urls = (
        ("article_list.html", '/article/<git_username>'),
        ("login.html", '/login'),
        ("register.html", '/register'),
        ("reset_password.html", "/reset_password"),
        ("index.html", '/'),
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
        article.Tag,
        githooks.GitHooks,
        user.User,
        bloguser.BlogUser,
        comment.Comment,
        userinfo.UserInfo,
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
    db.bind(app.config["DATABASE_NAME"], create_db=True, **params)
    db.generate_mapping(create_tables=True)


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
