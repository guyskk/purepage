# coding:utf-8

from __future__ import unicode_literals
from markdown import Markdown
from pyquery import PyQuery as pq
import os
from datetime import datetime
import logging


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


def read_articles(mddir):

    def get_meta(meta, key):
        return u"".join(meta.get(key, []))

    if not os.path.exists(mddir):
        logging.warning("Article dir not exists: %s" % mddir)
        return
    for fname in os.listdir(mddir):
        if os.path.splitext(fname)[1] != ".md":
            continue
        path = os.path.join(mddir, fname)
        try:
            content, toc, meta = parse_article(path)
        except Exception as e:
            logging.warning("Can't read %s: %s" % (path, e))
        else:
            keys = ["title", "subtitle", "date", "author"]
            m = {k: get_meta(meta, k) for k in keys}
            if not m["title"]:
                m["title"] = os.path.splitext(fname)[0]
            if not m["date"]:
                m["date"] = datetime.now().strftime(b"%Y年%m月%d日")
            tags = meta.get("tags", [])
            m["tags"] = tags
            yield (content, toc, m)
