# coding:utf-8

from __future__ import unicode_literals
import subprocess
import re
import os
from flask import request
from flask_restaction import Resource
import sys
from pony.orm import db_session
from . import app, db
from .util import read_articles
from . import model
import json


def git_dirname(url):
    dirname = re.findall(ur"^.*/(.*)\.git$", url)
    assert len(dirname) == 1, "dirname can't be found in repo_url"
    dirname = dirname[0]
    return dirname


def git_pull(dest, repo_url, remote_branch_name, encoding="utf-8"):
    ret = []
    dirname = git_dirname(repo_url)
    if not os.path.exists(dest):
        os.makedirs(dest)
    cwd = os.path.join(dest, dirname)
    if not os.path.exists(cwd):
        ret_git_clone = subprocess.check_output(
            ["git", "clone", repo_url], cwd=dest, shell=True)
        ret.append(ret_git_clone.decode(encoding))
    else:
        ret_git_pull = subprocess.check_output(
            ["git", "pull", repo_url, remote_branch_name],
            cwd=cwd, shell=True)
        ret.append(ret_git_pull.decode(encoding))

    return"\r\n".join(ret)


def init_db(mddir):

    def get_meta(meta, key):
        return u"".join(meta.get(key, []))

    db.drop_all_tables(with_all_data=True)
    db.create_tables()
    for content, toc, meta in read_articles(mddir):
        with db_session:
            m_tags = [model.Tag(name=tag) for tag in meta["tags"]]
            m_meta = model.ArticleMeta(**dict(meta, tags=m_tags))
            m_article = model.Article(
                content=content, toc=toc, meta=m_meta)


class GitHooks(Resource):

    """docstring for GitHooks"""

    def get(self):
        dest = app.config["ARTICLE_DEST"]
        repo_url = app.config["ARTICLE_REPO_URL"]
        branch = app.config["ARTICLE_REPO_BRANCH"]
        dirname = git_dirname(repo_url)
        subdir = app.config["ARTICLE_SUBDIR"]

        encoding = sys.stdout.encoding
        ret = git_pull(dest, repo_url, branch, encoding)
        data = request.get_json(force=False, silent=True, cache=True)

        init_db(os.path.join(dest, dirname, subdir))

        return {"ret": ret, "json": json.dumps(
            data, ensure_ascii=False, indent=2)}
