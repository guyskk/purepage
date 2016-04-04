# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from flask import abort, g
from flask_restaction import Resource
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from validater import validate
from . import auth, api, db
from .article_util import read_repo


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
        if userid in db:
            abort(400, "User Already Exists")
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

    def put_password(self, password, new_password):
        pass

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
