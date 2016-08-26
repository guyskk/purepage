from flask import g, abort
from flask_restaction import Resource
from purepage import db
from couchdb.http import NotFound, CouchdbException


class Article(Resource):
    """Article"""

    schema_article = {
        "_id": ("unicode&required", "文章ID"),
        "userid": ("unicode&required", "作者"),
        "catalog": ("unicode&required", "目录"),
        "article": ("unicode&required", "文章名称"),
        "title": ("unicode&required", "文章标题"),
        "summary": ("unicode", "文章摘要"),
        "tags": [("unicode&required", "标签")],
        "date": ("datetime&required&output", "创建/修改日期"),
        "content": ("unicode&required", "文章内容"),
    }

    schema_article_no_content = schema_article.copy()
    del schema_article_no_content['content']

    schema_article_create = schema_article.copy()
    del schema_article_create['_id']
    del schema_article_create['userid']

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
        },
        "post": schema_article_create
    }
    schema_outputs = {
        "get": schema_article,
        "get_list": {
            "total": "int&required",
            "offset": "int&required",
            "rows": [schema_article_no_content]
        },
        "post": schema_article,
    }

    def get(self, userid, catalog, article):
        """获取一篇文章"""
        key = ".".join([userid, catalog, article])
        result = db.get(key)
        return result

    def get_list(self, pagenum, pagesize, userid, catalog, tag):
        """
        获取文章列表，结果按时间倒序排序。

        过滤参数有以下组合：
        1. userid: 只返回指定作者的文章
        2. userid + catalog: 只返回指定作者的指定目录的文章
        3. userid + tag: 只返回指定作者的指定标签的文章
        4. tag: 只返回指定标签的文章
        """

        if userid:
            if tag:
                view = "by_user_tag"
                startkey = [userid, tag, {}]
                endkey = [userid, tag]
            elif catalog:
                view = "by_user_catalog"
                startkey = [userid, catalog, {}]
                endkey = [userid, catalog]
            else:
                view = "by_user"
                startkey = [userid, {}]
                endkey = [userid]
        elif tag:
            view = "by_tag"
            startkey = [tag, {}]
            endkey = [tag]
        else:
            view = "by_date"
            startkey = None
            endkey = {}
        params = {
            "reduce": False,
            "include_docs": True,
            "skip": (pagenum - 1) * pagesize,
            "limit": pagesize,
            "descending": True,
        }
        view = ("article", view)
        if startkey:
            params["startkey"] = startkey
            params["endkey"] = endkey
        result = db.query(view, **params)
        return {
            "total": result['total_rows'],
            "offset": result['offset'],
            "rows": [x['doc'] for x in result['rows']]
        }

    def post(self, catalog, article, **info):
        """创建或修改文章"""
        userid = g.user['_id']
        _id = '.'.join([userid, catalog, article])
        try:
            origin = db.get(_id)
        except NotFound:
            origin = {
                'type': 'article',
                '_id': _id,
                'userid': userid,
                'catalog': catalog,
                'article': article
            }
        origin.update(info)
        db.put(origin)
        return origin


@Article.error_handler
def handler_404(self, ex):
    if isinstance(ex, CouchdbException):
        if ex.status_code == 404:
            abort(404, '%s: %s' % (ex.error or 'Not Found', ex.reason or ''))
