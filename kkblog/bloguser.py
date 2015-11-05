# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import request
from flask.ext.restaction import Resource, abort, schema
from datetime import datetime
from pony.orm import select, db_session, count
from kkblog import model
from kkblog import user
import gitutil


@db_session
def user_role(user_id):
    u = model.BlogUser.get(user_id=user_id)
    if u is not None:
        return u.role


@db_session
def add_admin(user_id, article_repo):
    role = "bloguser.admin"
    u = model.BlogUser.get(user_id=user_id)
    if not u:
        return add_bloguser(user_id, role=role, article_repo=article_repo)
    else:
        return update_bloguser(user_id, role=role, article_repo=article_repo)


def add_bloguser(user_id, role, article_repo=None):
    u = model.BlogUser.get(user_id=user_id)
    if u:
        raise ValueError("bloguser user_id=%s already exists" % user_id)
    try:
        __, gitname, __ = gitutil.parse_giturl(article_repo)
    except:
        raise ValueError("invalid article_repo: %s" % article_repo)

    now = datetime.now()
    config = dict(user_id=user_id, role=role, article_repo=article_repo,
                  gitname=gitname, date_modify=now)
    u = model.BlogUser(date_create=now, **config)


def update_bloguser(user_id, **config):
    u = model.BlogUser.get(user_id=user_id)
    if not u:
        raise ValueError("bloguser user_id=%s not exists" % user_id)
    else:
        u.set(date_modify=datetime.now(), **config)
    return u


class BlogUser(Resource):
    """"""
    user_id = "int&required",
    role = "role_bloguser&required", "bloguser.normal"
    gitname = "unicode&required", None, "github 用户名"
    article_repo = "url&required", None, "文章的git仓库地址",
    latest_commit = "unicode", None, "最新一次提交的hash码"
    date_create = "iso_datetime&required"
    date_modify = "iso_datetime&required"
    schema_inputs = {
        "get": schema("user_id"),
        "get_me": None,
        "post": schema("article_repo"),
        "put": schema("article_repo"),
    }
    out = schema("user_id", "gitname", "article_repo", "role",
                 "latest_commit", "date_create", "date_modify")
    schema_outputs = {
        "get": out,
        "get_me": out,
        "post": out,
        "put": out,
    }

    @staticmethod
    def user_role(user_id):
        return user.user_role(user_id)

    def get(self, user_id):
        with db_session:
            u = model.BlogUser.get(user_id=user_id)
            if u is None:
                abort(404)
            return u.to_dict()

    def get_me(self):
        user_id = request.me["id"]
        with db_session:
            u = model.BlogUser.get(user_id=user_id)
            if u is None:
                abort(404)
            return u.to_dict()

    def post(self, article_repo):
        """创建BlogUser(开启个人博客)"""
        role = "bloguser.normal"
        user_id = request.me["id"]
        with db_session:
            try:
                u = add_bloguser(user_id, role, article_repo)
                return u.to_dict()
            except Exception as ex:
                abort(400, str(ex))

    def put(self, article_repo):
        """更新信息"""
        user_id = request.me["id"]
        with db_session:
            try:
                u = update_bloguser(user_id, article_repo)
                return u.to_dict()
            except Exception as ex:
                abort(400, str(ex))
