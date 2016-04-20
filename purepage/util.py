# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from flask import abort
from flask_mail import Message
from kkblog import markdown
from kkblog.exts import mail
import git
from git.repo.fun import is_git_dir
import giturlparse
import datetime
import os
import logging

logger = logging.getLogger(__name__)


def now():
    """Current datetime in ISO_8601 format string"""
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def send_mail(to, subject, html):
    """Send a html content mail"""
    logger.info("Send Mail To %s:\n" % to + html)
    msg = Message(subject, recipients=[to])
    msg.html = html
    try:
        mail.send(msg)
    except Exception as ex:
        logger.exception(ex)
        abort(500, "邮件发送失败: %s" % str(ex))


def read_articles(directory):
    """Parse articles from a directory, yield (meta, html) by generator.

    The directory can has subdirs, and the subdir which name
    contains '.' will be skiped, article filename must be end with '.md',
    article name can't contains '.'.

    This function will not raise Exceptions when encountered invalid file,
    it will just wran or info via logging.
    """
    for subdir in os.listdir(directory):
        dir_path = os.path.join(directory, subdir)
        if "." in subdir or not os.path.isdir(dir_path):
            logger.info("skip: %s" % subdir)
            continue
        for fname in os.listdir(dir_path):
            article_name, ext = os.path.splitext(fname)
            if ext != ".md":
                continue
            if "." in article_name:
                logger.warn("article name can't has '.': %s" % article_name)
                continue
            path = os.path.join(dir_path, fname)
            try:
                yield markdown.parse_article(path)
            except Exception as e:
                logger.warn("can't read %s: \n%s" % (path, e))


def read_repo(url, data_path):
    """Read articles from a git repo, save repo in data_path"""
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
            logger.warning(str(ex))
            if not ex.status == 128:
                raise
    else:
        repo = git.Repo.clone_from(url, repo_path)
    for x in read_articles(repo_path):
        yield x
