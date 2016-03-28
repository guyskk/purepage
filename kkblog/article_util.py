# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from markdown import Markdown
import os
import re
from datetime import datetime
from dateutil.parser import parse as date_parse
import git
import codecs
import giturlparse
import logging
from git.repo.fun import is_git_dir


def parse_article(path):
    """parse_article"""
    with codecs.open(path, encoding="utf-8") as f:
        source = f.read()
    extension_configs = {
        'markdown.extensions.codehilite': {'linenums': False},
    }
    md = Markdown(extensions=["markdown.extensions.meta", "markdown.extensions.codehilite"],
                  extension_configs=extension_configs)
    html = md.convert(source)
    meta = parse_meta(md.Meta, path)
    return html, meta


def parse_meta(meta, path):

    get_meta = lambda key: "".join(meta.get(key, []))

    def get_date(key):
        datestr = get_meta(key)
        date = None
        if datestr:
            try:
                date = date_parse(datestr)
            except Exception:
                logging.warning(
                    "[%s] invalid datetime format: %s" % (path, datestr))
        if date is None:
            date = datetime.utcnow()
        return date

    title = get_meta("title")
    fdir, fname = os.path.split(path)
    article_name = os.path.splitext(fname)[0]
    if not title:
        title = article_name
    date = get_date("date")
    tags = meta.get("tags", [])
    return {
        "catalog": os.path.basename(fdir),
        "article": article_name,
        "date": date,
        "title": title,
        "tags": tags
    }


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
                yield parse_article(path)
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
            logging.info(str(ex))
            if not ex.status == 128:
                raise
    else:
        repo = git.Repo.clone_from(url, repo_path)
    for x in read_articles(repo_path):
        yield x
