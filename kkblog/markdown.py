# coding:utf-8
"""Markdown."""
from __future__ import unicode_literals, absolute_import, print_function
import misaka
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os
import re
import datetime
import codecs
import logging
import yaml

logger = logging.getLogger(__name__)
META_END = re.compile(r"\n(\.{3}|-{3})")


def split_meta(text):
    """Split text into meta and content."""
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
        logger.warn("%s:\n%s" % (meta, ex))
        meta = {}
    return meta, text


class HighlighterRenderer(misaka.HtmlRenderer):
    """Code highlight."""

    def blockcode(self, text, lang):
        if not lang:
            assert type(text) is unicode
            try:
                return '\n<pre><code>{}</code></pre>\n'.format(text.strip())
            except UnicodeError:
                print(repr(text))
                raise
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)


def parse_article(path):
    """Parse article."""
    with codecs.open(path, encoding="utf-8") as f:
        source = f.read()
        assert type(source) is unicode
    meta, source = split_meta(source)
    extensions = misaka.EXT_TABLES | misaka.EXT_FENCED_CODE \
        | misaka.EXT_AUTOLINK | misaka.EXT_NO_INTRA_EMPHASIS
    md = misaka.Markdown(HighlighterRenderer(), extensions=extensions)
    html = md(source)
    meta = parse_meta(meta, path)
    return meta, html


def parse_meta(meta, path):
    meta = {k.lower(): v for k, v in meta.items()}

    def get_date():
        date = meta.get("date", None)
        if isinstance(date, datetime.date):
            date = datetime.datetime(*date.timetuple()[:3])
        if not isinstance(date, datetime.datetime):
            if date is not None:
                logger.warn("[%s] invalid datetime: %s" % (path, date))
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
        "tags": tags,
        "summary": meta.get("summary")
    }
