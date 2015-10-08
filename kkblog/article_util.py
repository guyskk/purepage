# coding:utf-8

from __future__ import unicode_literals
from markdown import Markdown
from pyquery import PyQuery as pq
import os
import re
from datetime import datetime
from dateutil.parser import parse as date_parse
from flask import current_app as app


def parse_article(path):
    """parse_article"""
    with open(path) as f:
        source = f.read()
    extension_configs = {
        'markdown.extensions.codehilite':
        {
            'linenums': False,
        },
    }

    md = Markdown(
        extensions=["markdown.extensions.toc",
                    "markdown.extensions.meta",
                    "markdown.extensions.codehilite"],
        extension_configs=extension_configs)
    html = md.convert(source.decode("utf-8"))
    d = pq(html)
    d.remove("div.toc")
    return d.html(), md.toc, md.Meta


def parse_meta(meta, path):

    get_meta = lambda key: "".join(meta.get(key, []))

    def get_date(key):
        datestr = get_meta(key)
        date = None
        try:
            date = date_parse(datestr)
        except Exception:
            app.logger.warning("[%s] invalid datetime format: %s" % (path, m["date"]))
        if date is None:
            date = os.path.getmtime(path)
        return date

    keys = ["title", "subtitle", "author"]
    fdir, fname = os.path.split(path)
    m = {k: get_meta(k) for k in keys}
    subdir = os.path.basename(fdir)
    m["subdir"] = subdir
    m["filename"] = fname
    if not m["title"]:
        m["title"] = os.path.splitext(fname)[0]
    m["date_create"] = get_date("date_create")
    m["date_modify"] = get_date("date_modify")
    m["tags"] = meta.get("tags", [])
    return m


def read_modified_articles(mddir, diff):
    modified_status = ["A", "M"]
    un_modified_status = ["C", "R", "T", "U", "X", "D"]
    for status, path in diff:
        if status not in modified_status:
            continue
        path = os.path.join(mddir, path)
        if not os.path.exists(path):
            app.logger.warning("File not exists: %s" % path)
            continue
        try:
            content, toc, meta = parse_article(path)
            m = parse_meta(meta, path)
            yield (content, toc, m)
        except Exception as e:
            app.logger.warning("Can't read %s: %s" % (path, e))


def read_articles(mddir):

    assert isinstance(mddir, unicode), "mddir must be unicode string"

    p_subdir = re.compile(r"^\w{4,16}$")
    if not os.path.exists(mddir):
        app.logger.warning("mddir not exists: %s" % mddir)
        return
    for subdir in os.listdir(mddir):
        dir_path = os.path.join(mddir, subdir)
        if not p_subdir.match(subdir) or not os.path.isdir(dir_path):
            app.logger.info("skip subdir: %s" % subdir)
            continue
        for fname in os.listdir(dir_path):
            if os.path.splitext(fname)[1] != ".md":
                continue
            path = os.path.join(dir_path, fname)
            try:
                content, toc, meta = parse_article(path)
                m = parse_meta(meta, path)
                yield (content, toc, m)
            except Exception as e:
                app.logger.warning("Can't read %s: %s" % (path, e))
