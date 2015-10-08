# coding:utf-8

from __future__ import unicode_literals
from flask_restaction import Resource, abort
from pony.orm import select, db_session, count
from kkblog import model


def _out_article(art):
    return {
        "content": art.content,
        "toc": art.toc,
        "meta": _out_meta(art.meta)
    }


def _out_meta(meta):
    tags = [t.name for t in meta.tags]
    git_username = meta.bloguser.git_username
    return dict(meta.to_dict(), tags=tags, git_username=git_username)


def get_article(git_username, subdir, filename):
    with db_session:
        user = model.BlogUser.get(git_username=git_username)
        if not user:
            return None
        meta = model.ArticleMeta.get(bloguser=user, subdir=subdir, filename=filename)
        if not meta:
            return None
        return _out_article(meta.article)


class Article(Resource):

    """文章Article"""
    s_pagenum = ("pagenum", {
        "desc": "第几页，从1开始计算",
        "required": True,
        "default": 1,
        "validate": "+int"})
    s_pagesize = ("pagesize", {
        "desc": "每页的文章数量",
        "required": True,
        "default": 10,
        "validate": "int"})
    s_id = ("id", {
        "desc": "文章ID",
        "required": True,
        "validate": "int"})
    s_git_username = ("git_username", {
        "required": True,
        "validate": "unicode"
    })
    s_subdir = ("subdir", {
        "required": True,
        "validate": "unicode"
    })
    s_filename = ("filename", {
        "desc": "markdown file name",
        "required": True,
        "validate": "unicode"
    })
    s_content = ("content", {
        "desc": "article content",
        "required": True,
        "validate": "unicode"
    })
    s_toc = ("toc", {
        "desc": "article table of content",
        "required": True,
        "validate": "unicode"
    })
    s_title = ("title", {
        "desc": "markdown file name",
        "required": True,
        "validate": "unicode"
    })
    s_subtitle = ("subtitle", {
        "validate": "unicode"
    })
    s_tags = ("tags", [{
        "validate": "unicode"
    }])

    s_date_create = ("date_create", {
        "validate": "iso_datetime"
    })
    s_date_modify = ("date_modify", {
        "validate": "iso_datetime"
    })
    s_author = ("author", {
        "validate": "unicode"
    })
    s_meta = ("meta", dict([s_git_username, s_subdir, s_filename,
                            s_title, s_subtitle, s_tags,
                            s_date_create, s_date_modify, s_author]))
    s_out = dict([s_meta, s_content, s_toc])

    schema_inputs = {
        "get": dict([s_git_username, s_subdir, s_filename]),
        "get_by_id": dict([s_id]),
        "get_list": dict([s_pagenum, s_pagesize]),
    }
    schema_outputs = {
        "get": dict([s_meta, s_content, s_toc]),
        "get_by_id": dict([s_meta, s_content, s_toc]),
        "get_list": [dict([s_meta])],
    }

    def get_list(self, pagenum, pagesize):
        """获取文章列表"""
        with db_session:
            metas = select(m for m in model.ArticleMeta).page(pagenum, pagesize)
            result = [{"meta": _out_meta(meta)} for meta in metas]
            return result

    def get(self, git_username, subdir, filename):
        """获取一篇文章"""
        art = get_article()
        if not art:
            abort(404)
        else:
            return art

    def get_by_id(self, id):
        with db_session:
            art = model.Article.get(id=id)
            if not art:
                abort(404)
            return _out_article(art)


class Tag(Resource):

    """文章标签"""
    s_name = ("name", {
        "desc": "标签名称",
        "validate": "unicode",
        "required": True
    })
    s_count = ("count", {
        "desc": "文章数量",
        "validate": "int",
        "required": True
    })
    schema_outputs = {
        "get_list": [dict([s_name, s_count])]
    }

    def get_list(self):
        """获取所有标签"""
        with db_session:
            out_tag = lambda t: {"name": t.name, "count": count(t.article_metas)}
            tags = [out_tag(t) for t in model.Tag.select()]
            return tags