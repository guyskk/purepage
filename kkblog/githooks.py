# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
import os
from flask import request, current_app
from flask_restaction import Resource, abort
import sys
from pony.orm import db_session
from kkblog import db
from kkblog.article_util import read_articles, read_modified_articles
from kkblog import model
from gitutil import gitutil
import json


def update_local(repo_url, owner):
    """从本地仓库读取文章，更新数据库内容"""
    dest = os.path.join(current_app.config["ARTICLE_DEST"], owner)
    if not os.path.exists(dest):
        os.makedirs(dest)
    return gitutil.pull_or_clone(repo_url, dest)


def _get_mtags(meta):
    m_tags = []
    for tag_name in meta["tags"]:
        tag = model.Tag.get(name=tag_name)
        if tag is None:
            tag = model.Tag(name=tag_name)
        m_tags.append(tag)
    return m_tags


def update_db(mddir, user_id, old_commit=None):

    # old_commit='' or None, initdb
    if not old_commit:
        _init_db(mddir, user_id)
        return
    diff = gitutil.modified_files(mddir, old_commit)

    def parse_path(path):
        fdir, fname = os.path.split(path)
        subdir = os.path.basename(fdir)
        return subdir, fname
    # delete files
    deleted_files = [parse_path(path) for status, path in diff
                     if status == "D"]
    for subdir, filename in deleted_files:
        with db_session:
            meta = model.ArticleMeta.get(subdir=subdir, filename=filename)
            if meta:
                meta.article.delete()

    # update files
    with db_session:
        u = model.BlogUser.get(user_id=user_id)
        if not u:
            abort(404)
        for content, toc, meta in read_modified_articles(mddir, diff):
            m_tags = _get_mtags(meta)
            m_meta = model.ArticleMeta.get(subdir=subdir, filename=filename)
            if m_meta:
                m_meta.set(**dict(meta, tags=m_tags))
                m_meta.article.set(content=content, toc=toc)
            else:
                m_meta = model.ArticleMeta(**dict(meta, tags=m_tags, bloguser=u))
                m_article = model.Article(
                    content=content, toc=toc, meta=m_meta)


def clear_db(user_id):
    with db_session:
        u = model.BlogUser.get(user_id=unicode(user_id))
        if not u:
            abort(404)
        for m in u.article_metas:
            m.article.delete()
        u.latest_commit = ""


def _init_db(mddir, user_id):
    with db_session:
        u = model.BlogUser.get(user_id=user_id)
        if not u:
            abort(404)
        for content, toc, meta in read_articles(mddir):
            m_tags = _get_mtags(meta)
            m_meta = model.ArticleMeta(**dict(meta, tags=m_tags, bloguser=u))
            m_article = model.Article(
                content=content, toc=toc, meta=m_meta)


def get_mddir(repo_url, dest=None):
    if dest is None:
        dest = current_app.config["ARTICLE_DEST"]
    host, owner, repo = gitutil.parse_giturl(repo_url)
    return os.path.join(dest, owner, repo)


class GitHooks(Resource):

    """GitHooks"""

    s_local = ("local", {
        "default": False,
        "desc": "是否从本地仓库更新",
        "validate": "bool"
    })
    s_rebuild = ("rebuild", {
        "default": False,
        "desc": "是否重新生成数据库信息",
        "validate": "bool"
    })
    schema_inputs = {
        "post": None,
        "post_update": dict([s_local, s_rebuild]),
    }

    @staticmethod
    def user_role(user_id):
        if user_id is None:
            return "*"
        with db_session:
            u = model.BlogUser.get(user_id=unicode(user_id))
            if u:
                return u.role
            else:
                return "*"

    def post(self):
        """响应github webhooks更新数据"""
        # data = request.get_json(force=False, silent=True, cache=True)
        return self.post_update()

    def post_update(self, local=False, rebuild=False):
        """强制更新数据库数据
        """
        user_id = unicode(request.me["id"])
        with db_session:
            u = model.BlogUser.get(user_id=user_id)
            if not u:
                abort(404)
            repo_url = u.article_repo
            old_commit = u.latest_commit
        if rebuild:
            clear_db(user_id)
            old_commit = ""
        msg = "local"
        err = None
        if not local:
            __, owner, __ = gitutil.parse_giturl(repo_url)
            err, ret = update_local(repo_url, owner)
            msg = err.message if err else ret
        if not err:
            mddir = get_mddir(repo_url)
            update_db(mddir, user_id, old_commit)
            logs = gitutil.git_log(mddir)
            if logs:
                latest_commit = logs[0][0]
                with db_session:
                    u = model.BlogUser.get(user_id=user_id)
                    u.latest_commit = latest_commit
        return {"message": msg, "success": bool(not err)}
