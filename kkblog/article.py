# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask.ext.restaction import Resource, abort, schema
from pony.orm import select, db_session, count
from kkblog import model
from kkblog import user
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


class Article(Resource):

    """文章Article

    gitname, subdir, filename 可以唯一确定一篇文章
    """
    user_id = "+int&required"
    pagenum = "+int&required", 1, "第几页，从1开始计算",
    pagesize = "+int&required", 10, "每页的数量"
    id = "int&required", None, "文章ID",
    gitname = "unicode&required"
    subdir = "unicode&required"
    filename = "unicode&required", None, "markdown file name",
    html = "unicode&required", None, "article content html",
    toc = "unicode&required", None, "article table of content",
    title = "unicode&required", None, "markdown file name",
    subtitle = "unicode"
    tag = "unicode"
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
    }
    schema_outputs = {
        "get": article_with_content,
        "get_by_id": article_with_content,
        "get_list": schema(["article"]),
        "get_list_by_user": schema(["article"]),
        "get_list_by_user_id": schema(["article"]),
    }

    @staticmethod
    def user_role(user_id):
        return user.user_role(user_id)

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
        with db_session:
            arts = model.Article.select().page(pagenum, pagesize)
            result = [output_article(art) for art in arts]
            return result

    @cache.cached(timeout=3)
    def get_list_by_user(self, gitname, pagenum, pagesize):
        """获取一个作者的文章列表"""
        with db_session:
            arts = model.Article.select(lambda x: x.gitname == gitname).page(pagenum, pagesize)
            result = [output_article(art) for art in arts]
            return result

    @cache.cached(timeout=3)
    def get_list_by_user_id(self, user_id, pagenum, pagesize):
        """获取一个作者的文章列表"""
        with db_session:
            bloguser = model.BlogUser.get(user_id=user_id)
            arts = bloguser.articles.page(pagenum, pagesize)
            result = [output_article(art) for art in arts]
            return result
