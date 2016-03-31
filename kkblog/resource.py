# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from flask import abort, g
from flask_restaction import Resource
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from validater import validate
from . import auth, api, db
from .article_util import read_repo


def now():
    dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def gen_pwdhash(password):
    return generate_password_hash(
        password, method='pbkdf2:sha256', salt_length=16)

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
schema_article = api.validater.parse(schema_article)


class Article(Resource):
    """Article"""

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


class Comment(Resource):
    """Comment"""
    schema_comment = {
        "userid": ("unicode&required", "评论者ID"),
        "userid": ("unicode&required", "评论者"),
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
            "rows": [dict(x.value["comment"].items() + x.doc.items()) for x in result]
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
        doc = db.get(_id, None)
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


class User(Resource):
    """User"""
    schema_user = {
        "_id": ("unicode&required", "用户ID"),
        "role": ("unicode&required", "角色"),
        "photo": ("unicode", "头像"),
        "repo": ("url", "博客仓库地址")
    }
    schema_inputs = {
        "get_me": None,
        "post_signup": {
            "userid": "unicode&required",
            "password": "password&required",
        },
        "post_login": {
            "userid": "unicode&required",
            "password": "password&required",
        },
        "put": {
            "repo": ("url&required", "博客仓库地址")
        },
        "post_sync_repo": None
    }
    schema_outputs = {
        "get_me": schema_user,
        "post_signup": "unicode&required",
        "post_login": schema_user,
        "put": schema_user,
        "post_sync_repo": {
            "succeed": ("int&required", "同步成功的文章数"),
            "errors": ("any", "错误")
        }
    }

    def __init__(self):
        self.userid = None
        self.user = None
        if g.token and "userid" in g.token:
            self.userid = g.token["userid"]
            self.user = db.get(g.token["userid"], None)

    def get_me(self):
        """获取自己的信息"""
        if self.user:
            return self.user
        abort(404, "Not Found")

    def post_signup(self, userid, password):
        """注册"""
        user = {
            "_id": userid,
            "role": "normal",
            "photo": "default.png",
            "pwdhash": gen_pwdhash(password)
        }
        db.save(user)
        return "OK"

    def post_login(self, userid, password):
        """登录"""
        user = db.get(userid, None)
        if user is None:
            abort(403, "User Not Exists")
        if not check_password_hash(user["pwdhash"], password):
            abort(403, "Password Incorrect")
        return user, auth.gen_header({"userid": userid})

    def put(self, repo):
        """修改个人信息"""
        self.user["repo"] = repo
        db.save(self.user)
        return self.user

    def post_sync_repo(self):
        """同步博客仓库

        需要先设置好自己的博客仓库地址（调用修改个人信息接口）。
        服务器会从仓库下载所有文件，并解析其中的 markdown 文件。
        再将解析后的文章内容和标题，日期等信息保存到数据库中。
        <pre>
        errors的结构为: 
            {
                "my_article": {
                    "title": "error reason",
                    "date": "error reason",
                    ...
                },
                "other_article": ...
            }
        </pre>
        """
        repo = self.user.get("repo")
        count = 0
        errors = {}
        if not repo:
            abort(400, "you didn't set your repo")
        for meta, content in read_repo(repo, "data"):
            key = ".".join([self.userid, meta["catalog"], meta["article"]])
            origin = db.get(key, {})
            changes = dict(meta)
            changes["userid"] = self.userid
            changes["_id"] = key
            changes["content"] = content
            err, changes = validate(changes, schema_article)
            if err:
                errors[changes["title"]] = dict(err)
            else:
                changes["type"] = "article"
                origin.update(changes)
                db.save(origin)
                count += 1
        return {
            "succeed": count,
            "errors": errors
        }
