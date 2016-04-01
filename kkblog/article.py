# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from flask import abort
from flask_restaction import Resource
from . import db


class Article(Resource):
    """Article"""
    schema_article = {
        "_id": ("unicode&required", "文章ID"),
        "userid": ("unicode&required", "作者"),
        "catalog": ("unicode&required", "目录"),
        "article": ("unicode&required", "文章名称"),
        "title": ("unicode&required", "文章标题"),
        "content": ("unicode&required", "文章内容"),
        "tags": [("unicode&required", "标签")],
        "date": ("datetime&required&output", "创建/修改日期")
    }
    schema_inputs = {
        "get": {
            "userid": ("unicode&required", "作者"),
            "catalog": ("unicode&required", "目录"),
            "article": ("unicode&required", "文章名称"),
        },
        "get_list": {
            "pagenum": ("+int&default=1", "第几页，从1开始计算"),
            "pagesize": ("+int&default=10", "每页的数量"),
            "userid": ("unicode", "作者"),
            "catalog": ("unicode", "目录"),
            "tag": ("unicode", "标签")
        }
    }
    schema_outputs = {
        "get": schema_article,
        "get_list": {
            "total": "int&required",
            "offset": "int&required",
            "rows": [schema_article]
        }
    }

    def get(self, userid, catalog, article):
        """获取一篇文章"""
        key = ".".join([userid, catalog, article])
        result = db.get(key, None)
        if result is None:
            abort(404, "Not Found")
        return result

    def get_list(self, pagenum, pagesize, userid, catalog, tag):
        """获取文章列表"""
        if userid:
            if tag:
                view = "article/by_user_tag"
                startkey = [userid, tag, {}]
                endkey = [userid, tag]
            elif catalog:
                view = "article/by_user_catalog"
                startkey = [userid, catalog, {}]
                endkey = [userid, catalog]
            else:
                view = "article/by_user"
                startkey = [userid, {}]
                endkey = [userid]
        elif tag:
            view = "article/by_tag"
            startkey = [tag, {}]
            endkey = [tag]
        else:
            view = "article/by_date"
            startkey = None
            endkey = {}
        params = {
            "reduce": False,
            "include_docs": True,
            "skip": (pagenum - 1) * pagesize,
            "limit": pagesize,
            "descending": True
        }
        if startkey:
            params["startkey"] = startkey
            params["endkey"] = endkey
        result = db.view(view, **params)
        return {
            "total": result.total_rows,
            "offset": result.offset,
            "rows": [x.doc for x in result]
        }
