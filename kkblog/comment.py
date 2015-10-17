# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask.ext.restaction import Resource, abort
from pony.orm import select, db_session, count
from kkblog import model
from kkblog import user


class Comment(Resource):
    """文章评论"""
    s_id = ("id", {
        "validate": "int",
        "required": True
    })
    s_username = ("username", {
        "validate": "re_email",
        "required": True
    })
    s_pagenum = ("pagenum", {
        "desc": "第几页，从1开始计算",
        "required": True,
        "default": 1,
        "validate": "+int"})
    s_pagesize = ("pagesize", {
        "desc": "每页的数量",
        "required": True,
        "default": 10,
        "validate": "+int"})
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
        "desc": "评论内容",
        "required": True,
        "validate": "unicode"
    })
    s_date = ("date", {
        "desc": "评论时间",
        "required": True,
        "validate": "iso_datetime"
    })
    s_nickname = ("nickname", {
        "desc": "评论者昵称",
        "required": True,
        "validate": "unicode"
    })
    s_photo_url = ("photo_url", {
        "desc": "评论者头像url",
        "required": True,
        "validate": "url"
    })

    s_out = dict([s_content, s_date, s_nickname, s_photo_url])

    schema_inputs = {
        "get": dict([s_id]),
        "get_list_by_user": dict([s_git_username, s_pagenum, s_pagesize]),
        "get_list_by_article": dict([s_git_username, s_subdir, s_filename, s_pagenum, s_pagesize]),
        "get_list_by_article_id": dict([s_id, s_pagenum, s_pagesize]),
    }
    schema_outputs = {
        "get": s_out,
        "get_list_by_user": [s_out],
        "get_list_by_article": [s_out],
        "get_list_by_article_id": [s_out],
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

    def get_list_by_user(self, git_username, pagenum, pagesize):
        """获取一个用户的评论"""
        with db_session:
            user = model.BlogUser.get(git_username=git_username)
            if user is None:
                abort(404)
            cmt_list = select(x for x in model.Comment if x.article_bloguser == user).page(pagenum, pagesize)
            return [x.to_dict() for x in cmt_list]

    def get_list_by_article(self, git_username, subdir, filename, pagenum, pagesize):
        """通过文章名称获取一篇文章的评论"""
        with db_session:
            user = model.BlogUser.get(git_username=git_username)
            if user is None:
                abort(404)
            cmt_list = select(x for x in model.Comment
                              if x.article_bloguser == user
                              and x.article_subdir == subdir
                              and x.article_filename == filename).page(pagenum, pagesize)
            return [x.to_dict() for x in cmt_list]

    def get_list_by_article_id(self, id, pagenum, pagesize):
        """通过文章id获取一篇文章的评论"""
        with db_session:
            user = model.BlogUser.get(user_id=unicode(id))
            if user is None:
                abort(404)
            cmt_list = select(x for x in model.Comment
                              if x.article_bloguser == user
                              and x.article_subdir == subdir
                              and x.article_filename == filename).page(pagenum, pagesize)
            return [x.to_dict() for x in cmt_list]
