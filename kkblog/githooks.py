# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
import os
from flask import request, current_app
from flask.ext.restaction import Resource, abort, schema
from pony.orm import db_session, flush
import gitutil
from kkblog.article_util import read_articles, read_modified_articles
from kkblog import model
from kkblog import bloguser


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


def update_db(mddir, gitname, old_commit=None):

    # old_commit='' or None, initdb
    if not old_commit:
        _init_db(mddir, gitname)
        return
    diff = gitutil.modified_files(mddir, old_commit)

    def parse_path(path):
        fdir, fname = os.path.split(path)
        subdir = os.path.basename(fdir)
        return subdir, fname

    deleted_files = [parse_path(path) for status, path in diff
                     if status == "D"]
    with db_session:
        u = model.BlogUser.get(gitname=gitname)
        if not u:
            abort(404, "bloguser gitname=%s not exists" % gitname)
        # delete files
        for subdir, fname in deleted_files:
            art = model.Article.get(gitname=gitname, subdir=subdir, filename=fname)
            if art is not None:
                art.delete()

        # update files
        for html, toc, meta in read_modified_articles(mddir, diff):
            m_tags = _get_mtags(meta)
            art = model.Article.get(gitname=gitname, subdir=meta["subdir"],
                                    filename=meta["filename"])
            if art is not None:
                # modified
                art.set(**dict(meta, tags=m_tags, bloguser=u))
                art.content.set(html=html, toc=toc)
            else:
                # add new
                art = model.Article(**dict(meta, tags=m_tags, gitname=gitname, bloguser=u))
                cont = model.ArticleContent(article=art, html=html, toc=toc)


def clear_db(gitname):
    with db_session:
        arts = model.Article.select(lambda x: x.gitname == gitname)
        for art in arts:
            art.delete()
        u = model.BlogUser.get(gitname=gitname)
        if u:
            u.latest_commit = ""


def _init_db(mddir, gitname):
    with db_session:
        u = model.BlogUser.get(gitname=gitname)
        if not u:
            abort(404, "bloguser gitname=%s not exists" % gitname)
        for html, toc, meta in read_articles(mddir):
            m_tags = _get_mtags(meta)
            art = model.Article(**dict(meta, tags=m_tags, gitname=gitname, bloguser=u))
            cont = model.ArticleContent(article=art, html=html, toc=toc)


def get_mddir(repo_url, dest=None):
    if dest is None:
        dest = current_app.config["ARTICLE_DEST"]
    host, owner, repo = gitutil.parse_giturl(repo_url)
    return os.path.join(dest, owner, repo)


def update(user_id, local=False, rebuild=False):
    with db_session:
        u = model.BlogUser.get(user_id=user_id)
        if not u:
            abort(404, "bloguser %s not exists" % user_id)
        repo_url = u.article_repo
        old_commit = u.latest_commit
        gitname = u.gitname
    if rebuild:
        clear_db(gitname)
        old_commit = ""
    msg = "local"
    err = None
    if not local:
        __, owner, __ = gitutil.parse_giturl(repo_url)
        err, ret = update_local(repo_url, owner)
        msg = unicode(err) if err else ret
    if not err:
        mddir = get_mddir(repo_url)
        update_db(mddir, gitname, old_commit)
        logs = gitutil.git_log(mddir)
        if logs:
            latest_commit = logs[0][0]
            with db_session:
                u = model.BlogUser.get(user_id=user_id)
                u.latest_commit = latest_commit
    return err, msg


class GitHooks(Resource):
    """GitHooks"""

    local = "bool", False, "是否从本地仓库更新"
    rebuild = "bool", False, "是否重新生成数据库信息"
    message = "unicode"
    schema_inputs = {
        "post": None,
        "post_update": schema("local", "rebuild"),
    }
    schema_outputs = {
        "post": schema("message"),
        "post_update": schema("message"),
    }

    @staticmethod
    def user_role(user_id):
        return bloguser.user_role(user_id)

    def post(self):
        """响应github webhooks更新数据"""
        # data = request.get_json(force=False, silent=True, cache=True)
        return self.post_update()

    def post_update(self, local, rebuild):
        """强制更新数据库数据
        """
        user_id = request.me["id"]
        err, msg = update(user_id, local, rebuild)
        if err:
            abort(400, str(err))
        else:
            return {"message": msg}
