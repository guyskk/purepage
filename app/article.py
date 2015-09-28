# coding:utf-8

from __future__ import unicode_literals
from flask_restaction import Resource, abort
from . import model
from pony.orm import select, db_session


class Article(Resource):

    """docstring for Article"""
    s_name = ("name", {
        "desc": "markdown file name",
        "required": True,
        "validate": "safestr"
    })
    s_content = ("content", {
        "desc": "article content",
        "required": True,
        "validate": "unicode"
    })
    s_toc = ("toc", {
        "desc": "article toc",
        "required": True,
        "validate": "unicode"
    })
    s_meta = ("meta", {
        "title": {
            "required": True,
            "validate": "unicode"
        },
        "subtitle": {
            "validate": "unicode"
        },
        "tags": [{
            "validate": "unicode"
        }],
        "date": {
            "validate": "unicode"
        },
        "author": {
            "validate": "unicode"
        },
    })
    s_out = dict([s_meta, s_content, s_toc])
    schema_inputs = {
        "get": dict([s_name]),
        "get_db": dict([s_name]),
    }
    schema_outputs = {
        "get": s_out,
        "get_db": s_out,
        "get_list": [s_meta[1]]
    }

    # output_types = [model.Article, model.ArticleMeta, model.Tag]

    def get_list(self):
        """获取文章列表"""
        with db_session:
            metas = select(m for m in model.ArticleMeta)[:]
            result = [_out_meta(meta) for meta in metas]
            return result

    def get(self, name):
        """获取一篇文章"""
        with db_session:
            sel = select(m for m in model.ArticleMeta if m.title == name)[:1]
            if(len(sel) == 0):
                abort(404)
            meta = sel[0]
            return _out(meta)


def _out(m):
    art = m.article
    return {
        "content": art.content,
        "toc": art.toc,
        "meta": _out_meta(m)
    }


def _out_meta(m):
    tags = [t.name for t in m.tags]
    return dict(m.to_dict(), tags=tags)


def get_article(name):
    with db_session:
        sel = select(m for m in model.ArticleMeta if m.title == name)[:1]
        if(len(sel) == 0):
            return None
        meta = sel[0]
        return _out(meta)
