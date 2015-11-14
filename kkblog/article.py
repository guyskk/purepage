# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import abort
from flask.ext.restaction import Resource, schema
from pony.orm import select, db_session, count
from kkblog import model
from kkblog import cache


def output_article(art, with_content=False):
    tags = [t.name for t in art.tags]
    if with_content:
        cont = art.content.to_dict(only="html, toc")
        return dict(art.to_dict(), tags=tags, content=cont)
    else:
        return dict(art.to_dict(), tags=tags)


@db_session
def get_article(gitname, subdir, filename):
    art = model.Article.get(gitname=gitname, subdir=subdir, filename=filename)
    if not art:
        abort(404)
    return output_article(art, with_content=True)


@db_session
def get_article_list(lamb, pagenum, pagesize):
    if lamb is not None:
        arts = model.Article.select(lamb).page(pagenum, pagesize)
    else:
        arts = model.Article.select().page(pagenum, pagesize)
    result = [output_article(art) for art in arts]
    return result


class Article(Resource):

    """文章Article

    gitname, subdir, filename 这三个参数可以唯一确定一篇文章
    """
    user_id = "+int&required"
    pagenum = "+int&required", 1, "第几页，从1开始计算",
    pagesize = "+int&required", 10, "每页的数量"
    id = "int&required", None, "文章ID",
    gitname = "unicode&required"
    gitname2 = "gitname", ("unicode",)
    subdir = "unicode&required"
    filename = "unicode&required", None, "markdown file name",
    html = "unicode&required", None, "article content html",
    toc = "unicode&required", None, "article table of content",
    title = "unicode&required", None, "markdown file name",
    subtitle = "unicode"
    tag = "unicode&required"
    keywords = "unicode&required"
    tags = schema(["tag"])
    date_create = "iso_datetime"
    date_modify = "iso_datetime"
    author = "unicode"
    content = schema("html", "toc")
    article_items = ["id", "gitname", "subdir", "filename", "title", "subtitle",
                     "tags", "date_create", "date_modify", "author"]
    article = schema(*article_items)
    article_with_content = schema("content", *article_items)
    schema_inputs = {
        "get": schema("gitname", "subdir", "filename"),
        "get_by_id": schema("id"),
        "get_list": schema("pagenum", "pagesize"),
        "get_list_by_user": schema("gitname", "pagenum", "pagesize"),
        "get_list_by_user_id": schema("user_id", "pagenum", "pagesize"),
        "get_list_by_subdir": schema("gitname", "subdir", "pagenum", "pagesize"),
        "get_list_by_tag": schema("gitname2", "tag", "pagenum", "pagesize"),
        "get_list_by_keywords": schema("gitname2", "keywords", "pagenum", "pagesize"),
    }
    schema_outputs = {
        "get": article_with_content,
        "get_by_id": article_with_content,
        "get_list": schema(["article"]),
        "get_list_by_user": schema(["article"]),
        "get_list_by_user_id": schema(["article"]),
        "get_list_by_subdir": schema(["article"]),
        "get_list_by_tag": schema(["article"]),
        "get_list_by_keywords": schema(["article"]),
    }

    @cache.cached(timeout=3)
    def get(self, gitname, subdir, filename):
        """获取一篇文章"""
        return get_article(gitname, subdir, filename)

    @cache.cached(timeout=3)
    def get_by_id(self, id):
        """获取一篇文章"""
        with db_session:
            art = model.Article.get(id=id)
            if art is None:
                abort(404)
            return output_article(art, with_content=True)

    @cache.cached(timeout=3)
    def get_list(self, pagenum, pagesize):
        """获取文章列表"""
        return get_article_list(None, pagenum, pagesize)

    @cache.cached(timeout=3)
    def get_list_by_user(self, gitname, pagenum, pagesize):
        """获取一个作者的文章列表"""
        return get_article_list(lambda x: x.gitname == gitname, pagenum, pagesize)

    @cache.cached(timeout=3)
    def get_list_by_user_id(self, user_id, pagenum, pagesize):
        """获取一个作者的文章列表"""
        with db_session:
            bloguser = model.BlogUser.get(user_id=user_id)
            arts = bloguser.articles.page(pagenum, pagesize)
            result = [output_article(art) for art in arts]
            return result

    @cache.cached(timeout=3)
    def get_list_by_subdir(self, gitname, subdir, pagenum, pagesize):
        """获取一个作者的文章归档"""
        return get_article_list(lambda x: x.gitname == gitname and x.subdir == subdir,
                                pagenum, pagesize)

    @cache.cached(timeout=3)
    def get_list_by_tag(self, gitname, tag, pagenum, pagesize):
        """按标签和作者查找文章，不指定 gitname 或者 gitname 为空字符串表示不限制文章作者"""
        with db_session:
            tag = model.Tag.get(name=tag)
            if gitname:
                lamb = lambda x: x.gitname == gitname and tag in x.tags
            else:
                lamb = lambda x: tag in x.tags
            return get_article_list(lamb, pagenum, pagesize)

    @cache.cached(timeout=3)
    def get_list_by_keywords(self, gitname, keywords, pagenum, pagesize):
        """按关键字查找文章，不指定 gitname 或者 gitname 为空字符串表示不限制文章作者"""
        if gitname:
            lamb = lambda x: x.gitname == gitname and keywords in x.title
        else:
            lamb = lambda x: keywords in x.title
        return get_article_list(lamb, pagenum, pagesize)
