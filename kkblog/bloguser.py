# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import request, url_for
from flask_restaction import Resource, abort
from datetime import datetime
from pony.orm import select, db_session, count
from kkblog import model
import gitutil


def _out_user(u):
    return u.to_dict()


def _get_user(user_id):
    with db_session:
        u = model.BlogUser.get(user_id=unicode(user_id))
        if not u:
            abort(404)
        return _out_user(u)


def add_admin(user_id, article_repo):
    role = "bloguser.admin"
    user_id = unicode(user_id)
    return create_or_update_bloguser(user_id, role, article_repo, website="")


def create_or_update_bloguser(user_id, role, article_repo, website):
    website = website or ""
    try:
        __, git_username, __ = gitutil.parse_giturl(article_repo)
    except:
        abort(400, "invalid article_repo: %s" % article_repo)
    user_id = unicode(user_id)
    config = dict(role=role, article_repo=article_repo,
                  git_username=git_username,
                  website=website, user_system="kkblog", user_id=user_id)
    with db_session:
        u = model.BlogUser.get(user_id=user_id)
        if not u:
            u = model.BlogUser(date_create=datetime.now(), **config)
        else:
            u.set(**config)
        return _out_user(u)


class BlogUser(Resource):
    """"""
    s_user_id = ("user_id", {
        "validate": "unicode",
        "required": True
    })
    s_role = ("role", {
        "validate": "bloguser_role",
        "required": True,
        "default": "bloguser.normal"
    })
    s_article_repo = ("article_repo", {
        "desc": "文章的git仓库地址",
        "validate": "url",
        "required": True
    })
    s_git_username = ("git_username", {
        "required": True,
        "validate": "unicode"
    })
    s_website = ("website", {
        "validate": "url",
    })
    s_latest_commit = ("latest_commit", {
        "validate": "unicode"
    })
    s_git_username = ("git_username", {
        "required": True,
        "validate": "unicode"
    })
    s_date_create = ("date_create", {
        "required": True,
        "validate": "iso_datetime"
    })
    s_user_system = ("user_system", {
        "required": True,
        "validate": "unicode"
    })
    schema_inputs = {
        "get": dict([s_user_id]),
        "get_me": None,
        "post": dict([s_role, s_article_repo, s_website]),
    }
    s_out = dict([s_user_system, s_user_id, s_git_username,
                  s_article_repo, s_role, s_latest_commit,
                  s_website, s_date_create])
    schema_outputs = {
        "get": s_out,
        "get_me": s_out,
        "post": s_out,
    }

    @staticmethod
    def user_role(user_id):
        if user_id is None:
            return "*"
        with db_session:
            u = model.User.get(id=user_id)
            if u:
                return u.role
            else:
                return "*"

    def get(self, user_id):
        return _get_user(user_id)

    def get_me(self):
        user_id = request.me["id"]
        return _get_user(user_id)

    def post(self, article_repo, website):
        """开启个人博客或更新资料"""
        role = "bloguser.normal"
        user_id = request.me["id"]
        return create_or_update_bloguser(user_id, role, article_repo, website)
