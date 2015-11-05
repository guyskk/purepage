# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import request
from flask.ext.restaction import Resource, abort, schema
from pony.orm import select, db_session, count
from kkblog import model
from kkblog import user
from datetime import datetime


def output_comments(comments):
    def output(x):
        user = model.User.get(id=x.user_id)
        return dict(x.to_dict(), userinfo=user.userinfo.to_dict())
    return [output(x) for x in comments]


def add_comment(art, content):
    if art is None:
        abort(404, "article not exists")
    now = datetime.now()
    info = {
        "gitname": art.gitname,
        "subdir": art.subdir,
        "filename": art.filename,
        "content": content,
        "user_id": request.me["id"],
        "date_create": now,
        "date_modify": now,
    }
    cmt = model.Comment(article=art, bloguser=art.bloguser, **info)
    return cmt


class Comment(Resource):
    """文章评论

    gitname, subdir, filename 这三个参数可以唯一确定一篇文章
    """
    id = "int&required", None
    user_id = "int&required", None, "评论者id"
    pagenum = "+int&required", 1, "第几页，从1开始计算"
    pagesize = "+int&required", 10, "每页的数量"
    gitname = "unicode&required"
    subdir = "unicode&required"
    filename = "unicode&required", None, "markdown file name"
    content = "unicode&required", None, "评论内容"
    date_create = "iso_datetime&required", None, "评论时间"
    date_modify = "iso_datetime&required", None, "评论修改时间"

    photo_url = "url"
    nickname = "unicode"

    comment = schema("id", "gitname", "subdir", "filename", "content",
                     "user_id", "date_create", "date_modify")
    userinfo = schema("photo_url", "nickname")
    comment_of_list = schema("id", "content", "user_id", "userinfo",
                             "date_create", "date_modify")
    schema_inputs = {
        "get": schema("id"),
        "get_list": schema("id", "pagenum", "pagesize"),
        "get_list_by3": schema("gitname", "subdir", "filename", "pagenum", "pagesize"),
        "get_list_of_me": schema("pagenum", "pagesize"),
        "get_list_to_me": schema("pagenum", "pagesize"),
        "post": schema("id", "content"),
        "post_by3": schema("gitname", "subdir", "filename", "content"),
        "put": schema("id", "content")
    }
    schema_outputs = {
        "get": comment,
        "get_list": schema(["comment_of_list"]),
        "get_list_by3": schema(["comment_of_list"]),
        "get_list_of_me": schema(["comment_of_list"]),
        "get_list_to_me": schema(["comment_of_list"]),
        "post": comment,
        "post3": comment,
        "put": comment
    }

    @staticmethod
    def user_role(user_id):
        return user.user_role(user_id)

    def get(self, id):
        """获取一个评论"""
        with db_session:
            cmt = model.Comment.get(id=id)
            if cmt is None:
                abort(404)
            return cmt.to_dict()

    def get_list(self, id, pagenum, pagesize):
        """通过文章id获取一篇文章的评论"""
        with db_session:
            art = model.Article.get(id=id)
            if art is None:
                abort(404)
            comments = art.comments.page(pagenum, pagesize)
            return output_comments(comments)

    def get_list_by3(self, gitname, subdir, filename, pagenum, pagesize):
        """通过gitname, subdir, filename获取一篇文章的评论"""
        with db_session:
            art = model.Article.get(gitname=gitname, subdir=subdir, filename=filename)
            if art is None:
                abort(404)
            comments = art.comments.page(pagenum, pagesize)
            return output_comments(comments)

    def get_list_of_me(self, pagenum, pagesize):
        """获取我发表的评论"""
        user_id = request.me["id"]
        with db_session:
            comments = model.Comment.select(lambda x: x.user_id == user_id)\
                .page(pagenum, pagesize)
            return output_comments(comments)

    def get_list_to_me(self, pagenum, pagesize):
        """获取别人对我文章的评论"""
        user_id = request.me["id"]
        with db_session:
            user = model.BlogUser.get(user_id=user_id)
            if user is None:
                abort(404)
            comments = user.comments.page(pagenum, pagesize)
            return output_comments(comments)

    def post(self, id, content):
        """添加评论, id 是 article_id"""
        with db_session:
            art = model.Article.get(id=id)
            cmt = add_comment(art, content)
            return cmt.to_dict()

    def post_by3(self, gitname, subdir, filename, content):
        """添加评论, 由gitname, subdir, filename这3个参数确定哪篇文章"""
        with db_session:
            art = model.Article.get(gitname=gitname, subdir=subdir, filename=filename)
            cmt = add_comment(art, content)
            return cmt.to_dict()

    def put(self, id, content):
        """修改评论, id 是 comment_id"""
        with db_session:
            cmt = model.Comment.get(id=id)
            if cmt is None:
                abort(404)
            now = datetime.now()
            info = {
                "content": content,
                "date_modify": now,
            }
            cmt.set(**info)
            return cmt.to_dict()
