# coding:utf-8
"""Comment"""
from __future__ import unicode_literals, absolute_import, print_function
from datetime import datetime
from flask import abort, g
from flask_restaction import Resource
from . import db


def now():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class Comment(Resource):
    """Comment"""
    schema_comment = {
        "userid": ("unicode&required", "评论者ID"),
        "photo": ("unicode&required", "评论者头像"),
        "content": ("unicode&required", "评论内容"),
        "date": ("datetime&required&output", "评论日期"),
    }
    schema_inputs = {
        "get": {
            "pagenum": ("+int&default=1", "第几页，从1开始计算"),
            "pagesize": ("+int&default=10", "每页的数量"),
            "article_id": ("unicode&required", "文章ID"),
        },
        "post": {
            "article_id": ("unicode&required", "文章ID"),
            "content": ("unicode&required", "评论内容"),
        }
    }
    schema_outputs = {
        "get": {
            "total": ("int&required", "总数(包括未返回的结果)"),
            "offset": ("int&required", "offset"),
            "rows": [schema_comment]
        },
        "post": schema_comment
    }

    def __init__(self):
        if g.token and "userid" in g.token:
            self.userid = g.token["userid"]
            self.user = db.get(self.userid, None)

    def format_result(self, result):
        return {
            "total": result.total_rows,
            "offset": result.offset,
            "rows": [dict(x.value["comment"].items() + x.doc.items())
                     for x in result]
        }

    def get(self, pagenum, pagesize, article_id):
        """获取一篇文章的评论"""
        params = {
            "reduce": False,
            "include_docs": True,
            "skip": (pagenum - 1) * pagesize,
            "limit": pagesize,
            "descending": True,
            "startkey": [article_id, {}],
            "endkey": [article_id]
        }
        result = db.view("comment/by_article", **params)
        return self.format_result(result)

    def post(self, article_id, content):
        """发表评论"""
        doc = db.get(article_id, None)
        if doc is None:
            abort(400, "Article Not Found")
        cmt = {
            "date": now(),
            "content": content,
            "userid": self.userid
        }
        doc.comments.append(cmt)
        db.save(doc)
        return dict(cmt.items() + self.user.items())

    def get_my(self, pagenum, pagesize):
        """获取我的评论：我发表的和别人对我的"""
        params = {
            "reduce": False,
            "include_docs": True,
            "skip": (pagenum - 1) * pagesize,
            "limit": pagesize,
            "descending": True,
            "startkey": [self.userid, {}],
            "endkey": [self.userid]
        }
        result = db.view("comment/by_user", **params)
        return self.format_result(result)
