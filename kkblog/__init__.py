# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

from flask import Flask, Blueprint, abort, current_app
from pony.orm import sql_debug, db_session
import re
import os
from datetime import datetime
from validater import add_validater

from kkblog.extensions import api, db
from kkblog import model
from kkblog import user
from kkblog import bloguser
from kkblog import userinfo
from kkblog import article
from kkblog import comment
from kkblog import githooks

__all__ = ["create_app", "api", "db"]


def create_app():
    app = Flask(__name__)
    config_app(app)
    bp_api = Blueprint('api', __name__, static_folder='static')
    api_config = {
        "bootstrap": "/static/lib/bootstrap.css",
        "permission_path": "config/permission.json",
        "auth_secret": app.config["API_AUTH_SECRET"],
    }
    api.init_app(bp_api, **api_config)

    config_validater(app)
    config_view(app)
    config_api(app)
    config_db(app)
    config_error_handler(app)
    config_before_handler(app)

    app.register_blueprint(bp_api, url_prefix='/api')
    return app


def config_app(app):
    app.config.from_object('kkblog.config.default_config')
    if 'KKBLOG_CONFIG' in os.environ:
        app.config.from_envvar('KKBLOG_CONFIG')
    app.config["ARTICLE_DEST"] = os.path.join(app.root_path, app.config["ARTICLE_DEST"])
    # pony_orm debug 信息
    if app.config["DEBUG"]:
        sql_debug(True)
    # 跨域
    if app.config["ALLOW_CORS"]:
        from flask.ext.cors import CORS
        CORS(app)
    # create data dir
    dir_data = os.path.join(app.root_path, "data")
    if not os.path.exists(dir_data):
        os.makedirs(dir_data)


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
            contents = f.read()
            contents = contents.decode("utf-8")\
                .replace('{{"article_title"}}', title)\
                .replace('{{"article_content"}}', cont)\
                .replace('{{"article_toc"}}', toc)
            return contents

    view_urls = (
        ("article_list.html", '/article/<git_username>'),
        ("login.html", '/login'),
        ("register.html", '/register'),
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
    db.bind(app.config["DATABASE_NAME"],
            app.config["DATABASE_PATH"],
            create_db=True)
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
