"""Comment"""
from flask import json, abort, g
from flask_restaction import Resource
from couchdb.http import NotFound
from purepage import db, util


class Comment(Resource):
    """Comment"""
    schema_comment = {
        "user": {
            "_id": ("unicode&required", "评论者ID"),
            "photo": ("unicode&default='/static/image/photo-default.png'",
                      "评论者头像"),
        },
        "content": ("unicode&required", "评论内容"),
        "date": ("datetime&required&output", "评论日期"),
    }
    schema_inputs = {
        "get": {
            "pagenum": ("+int&default=1", "第几页，从1开始计算"),
            "pagesize": ("+int&default=10", "每页的数量"),
            "article": ("unicode&required", "文章ID"),
        },
        "post": {
            "article": ("unicode&required", "文章ID"),
            "content": ("unicode&required", "评论内容"),
        }
    }
    schema_outputs = {
        "get": {
            "total_rows": ("int&required", "总数(包括未返回的结果)"),
            "offset": ("int&required", "offset"),
            "rows": [schema_comment]
        },
        "post": schema_comment
    }

    def format_comment(self, cmt):
        """convert couchdb view comment/by_article result to schema_comment"""
        user = cmt['doc']
        cmt = cmt['value']['comment']
        cmt['user'] = user
        return cmt

    def get(self, pagenum, pagesize, article):
        """获取一篇文章的评论"""
        params = {
            "reduce": False,
            "include_docs": True,
            "skip": (pagenum - 1) * pagesize,
            "limit": pagesize,
            "descending": True,
            "startkey": json.dumps([article, {}], ensure_ascii=False),
            "endkey": json.dumps([article], ensure_ascii=False)
        }
        result = db.query(("comment", "by_article"), **params)
        return {
            'total_rows': result['total_rows'],
            'offset': result['offset'],
            'rows': [self.format_comment(x) for x in result['rows']]
        }

    def post(self, article, content):
        """发表评论"""
        try:
            db.get(article)
        except NotFound:
            abort(400, "Article Not Found")
        date = util.now()
        _id = '.'.join([article, date, g.userid])
        cmt = {
            "_id": _id,
            "type": "comment",
            "article": article,
            "date": date,
            "content": content,
            "userid": g.userid
        }
        db.put(cmt)
        cmt['user'] = g.user
        return cmt
