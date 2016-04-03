# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
import misaka
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os
import re
import datetime
import git
import codecs
import giturlparse
import logging
from git.repo.fun import is_git_dir
import re
import yaml
import logging

META_END = re.compile(r"\n(\.{3}|-{3})")


def split_meta(text):
    if text[0:3] != '---':
        return {}, text
    meta_text = META_END.split(text[3:], 1)
    # meta_text: ['title: xx', '---', '\n# xxx']
    if len(meta_text) != 3:
        return {}, text
    meta, __, text = meta_text
    text = text.strip('\n')
    try:
        meta = yaml.load(meta)
    except yaml.YAMLError as ex:
        logging.warning("%s:\n%s" % (meta, ex))
        meta = {}
    return meta, text


class HighlighterRenderer(misaka.HtmlRenderer):
    """code highlight"""
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.encode("utf8").strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)


def parse_article(path):
    """parse_article"""
    with codecs.open(path, encoding="utf-8") as f:
        source = f.read()
    meta, source = split_meta(source)
    extensions = misaka.EXT_TABLES | misaka.EXT_FENCED_CODE \
        | misaka.EXT_AUTOLINK | misaka.EXT_NO_INTRA_EMPHASIS
    md = misaka.Markdown(HighlighterRenderer(), extensions=extensions)
    html = md(source)
    return parse_meta(meta, path), html


def parse_meta(meta, path):
    meta = {k.lower(): v for k, v in meta.items()}

    def get_date():
        date = meta.get("date", None)
        if isinstance(date, datetime.date):
            date = datetime.datetime(*date.timetuple()[:3])
        if not isinstance(date, datetime.datetime):
            if date is not None:
                logging.warning("[%s] invalid datetime: %s" % (path, date))
            date = datetime.datetime.utcnow()
        return date

    title = meta.get("title")
    fdir, fname = os.path.split(path)
    article_name = os.path.splitext(fname)[0]
    if not title:
        title = article_name
    date = get_date()
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
            logging.warning(str(ex))
            if not ex.status == 128:
                raise
    else:
        repo = git.Repo.clone_from(url, repo_path)
    for x in read_articles(repo_path):
        yield x
