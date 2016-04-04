# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from flask import current_app
from flask_mail import Message
from kkblog import markdown
from kkblog.exts import mail, db
import git
from git.repo.fun import is_git_dir
import giturlparse
import re
import datetime
import os
import logging


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def send_mail(to, subject, html):
    if current_app.debug:
        current_app.logger.info("Send Mail To %s:\n" % to + html)
    msg = Message(subject, recipients=[to])
    msg.html = html
    mail.send(msg)


def couchdb_count(view, key):
    """统计key的数量"""
    result = db.view(view, key=key)
    if result.total_rows == 0:
        return 0
    else:
        assert result.total_rows == 1, "Key Not Unique On Reduce View"
        return result[key].value


def read_articles(repo_path):

    assert isinstance(repo_path, unicode), "repo_path must be unicode string"

    p_catalog = re.compile(r"^\w{1,16}$")
    for subdir in os.listdir(repo_path):
        dir_path = os.path.join(repo_path, subdir)
        if not p_catalog.match(subdir) or not os.path.isdir(dir_path):
            logging.info("skip: %s" % subdir)
            continue
        for fname in os.listdir(dir_path):
            logging.debug("join: %s & %s" % (type(dir_path), type(fname)))
            if not isinstance(fname, unicode):
                logging.debug("fname not unicode")
                logging.debug(fname)
                continue
            if os.path.splitext(fname)[1] != ".md":
                continue
            path = os.path.join(dir_path, fname)
            try:
                yield markdown.parse_article(path)
            except Exception as e:
                logging.warning("Can't read %s: %s" % (path, e))


def read_repo(url, data_path):
    p = giturlparse.parse(url)
    assert p.valid, "git url %s invalid" % url
    repo_path = os.path.abspath(os.path.join(
        data_path, "%s.%s" % (p.owner, p.host)))
    if is_git_dir(os.path.join(repo_path, ".git")):
        repo = git.Repo.init(repo_path)
        assert not repo.bare
        try:
            repo.git.fetch()
            repo.git.merge()
            # repo.git.pull(["--git-dir=%s" % repo_path])
        except git.exc.GitCommandError as ex:
            logging.warning(str(ex))
            if not ex.status == 128:
                raise
    else:
        repo = git.Repo.clone_from(url, repo_path)
    for x in read_articles(repo_path):
        yield x
