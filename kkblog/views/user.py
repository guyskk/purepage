# coding:utf-8
"""User API"""
from __future__ import unicode_literals, absolute_import, print_function
import jwt
import couchdb
from datetime import datetime, timedelta
from flask import abort, g, current_app, render_template
from flask_restaction import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from validater import validate
from kkblog import auth, api, db
from kkblog import util


class InvalidTokenError(Exception):
    """token invalid"""


def gen_pwdhash(password):
    """生成密码hash"""
    return generate_password_hash(
        password, method='pbkdf2:sha256', salt_length=16)


def decode_token(token):
    """解码json web token"""
    auth_secret = current_app.config["USER_AUTH_SECRET"]
    auth_alg = current_app.config["USER_AUTH_ALG"]
    options = {
        'require_exp': True,
    }
    try:
        tk = jwt.decode(token, auth_secret,
                        algorithms=[auth_alg], options=options)
    except AttributeError as ex:
        raise InvalidTokenError("Invalid token" % str(ex))
    except jwt.InvalidTokenError as ex:
        raise InvalidTokenError(str(ex))
    return tk


def encode_token(token, exp=1800):
    """编码json web token"""
    auth_secret = current_app.config["USER_AUTH_SECRET"]
    auth_alg = current_app.config["USER_AUTH_ALG"]
    token['exp'] = datetime.utcnow() + timedelta(seconds=exp)
    token = jwt.encode(token, auth_secret, algorithm=auth_alg)
    return token.decode('utf-8')


schema_article = {
    "_id": ("unicode&required", "文章ID"),
    "userid": ("unicode&required", "作者"),
    "catalog": ("unicode&required", "目录"),
    "article": ("unicode&required", "文章名称"),
    "title": ("unicode&required", "文章标题"),
    "content": ("unicode&required", "文章内容"),
    "summary": ("unicode", "文章摘要"),
    "tags": [("unicode&required", "标签")],
    "date": ("datetime&required&output", "创建/修改日期"),
}
schema_article = api.validater.parse(schema_article)


class User(Resource):
    """User API

    注册分两步：
        1. post_verify 会发送注册链接到用户邮箱，链接中包含 userid 和 token
        2. post_signup 从链接中获取 userid 和 token，并在界面上显示 userid

    找回密码分两步：
        1. post_forgot 会发送重置链接到用户邮箱，链接中包含 userid 和 token
        2. post_reset 从链接中获取 userid 和 token，并在界面上显示 userid

    修改密码或邮箱：
        put_security 需验证密码

    注意：注册和找回密码的 token 不能互用

    token 解码后的格式:

        {
            "type": "signup/reset",
            "userid": "用户ID",
            "email": "邮箱",
            "exp": "过期时间"
        }

    """
    schema_user = {
        "_id": ("unicode&required", "用户ID"),
        "role": ("unicode&required", "角色"),
        "photo": ("unicode", "头像"),
        "repo": ("url", "博客仓库地址")
    }
    schema_inputs = {
        "get": {
            "userid": "unicode&required"
        },
        "get_me": None,
        "post_verify": {
            "userid": "unicode&required",
            "email": "email&required"
        },
        "post_signup": {
            "token": "unicode&required",
            "password": "password&required",
        },
        "post_login": {
            "userid": "unicode&required",
            "password": "password&required",
            "expiration": ("int(10,21600)&default=30", "过期时间(分钟)")
        },
        "post_forgot": {
            "email": "email&required"
        },
        "post_reset": {
            "token": "unicode&required",
            "password": "password&required",
        },
        "put_security": {
            "password": "password",
            "new_password": "password",
            "new_email": "email"
        },
        "put": {
            "repo": ("url", "博客仓库地址"),
            "photo": ("url", "头像"),
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
        """用户API"""
        self.userid = None
        self.user = None
        if g.token and "userid" in g.token:
            self.userid = g.token["userid"]
            self.user = db.get(self.userid)

    def get(self, userid):
        """获取用户信息"""
        user = db.get(userid)
        if user is not None:
            return user
        abort(404, "Not Found")

    def get_me(self):
        """获取自己的信息"""
        if self.user is not None:
            return self.user
        abort(404, "Not Found")

    def post_verify(self, userid, email):
        """验证用户名和邮箱"""
        token = {
            "type": "signup",
            "userid": userid,
            "email": email
        }
        if userid in db:
            abort(400, "UserID Already SignUp")
        if util.couchdb_count("user/email", key=email) >= 1:
            abort(400, "Email Already SignUp")
        token = encode_token(token)
        server = current_app.config["SERVER_URL"]
        link = "{server}/signup?userid={userid}&token={token}"\
            .format(server=server, token=token, userid=userid)
        html = render_template("mail-signup.html", link=link)
        util.send_mail(email, "Kkblog注册", html)
        return "注册链接已发送至您的邮箱"

    def post_signup(self, token, password):
        """注册"""
        token = decode_token(token)
        if token["type"] != "signup":
            abort(400, "Token Type Incorrect")
        if token["userid"] in db:
            abort(400, "UserID Already SignUp")
        user = {
            "_id": token["userid"],
            "role": "normal",
            "email": token["email"],
            "pwdhash": gen_pwdhash(password),
            "photo": "/static/image/photo-default.png",
            "date_create": util.now()
        }
        try:
            user = db.save(user)
        except couchdb.ResourceConflict:
            abort(400, "UserID Conflict")
        # check after save
        if util.couchdb_count("email/_count", key=token["email"]) > 1:
            db.delete(user)
            abort(400, "Email Already SignUp")
        return "OK", 201

    def post_login(self, userid, password, expiration):
        """登录"""
        user = db.get(userid)
        if user is None:
            abort(403, "User Not Exists")
        if not check_password_hash(user["pwdhash"], password):
            abort(403, "Password Incorrect")
        auth_exp = expiration * 60
        return user, auth.gen_header({"userid": userid}, auth_exp=auth_exp)

    def post_forgot(self, email):
        """忘记密码"""
        params = {
            "reduce": False,
            "include_docs": True,
            "key": email
        }
        result = db.view("user/by_email", **params)
        if result.total_rows == 0:
            abort(400, "User Not Exists")
        else:
            if result.total_rows != 1:
                abort(500, "Duplicate Email")
            user = result[email].doc
        token = {
            "type": "reset",
            "userid": user["_id"],
            "email": email
        }
        token = encode_token(token)
        server = current_app.config["SERVER_URL"]
        link = "{server}/reset?userid={userid}&token={token}"\
            .format(server=server, token=token, userid=user["_id"])
        html = render_template("mail-reset.html", link=link)
        util.send_mail(email, "Kkblog重置密码", html)
        return "重置密码链接已发送至您的邮箱"

    def post_reset(self, token, password):
        """重置密码"""
        token = decode_token(token)
        if token["type"] != "reset":
            abort(400, "Token Type Incorrect")
        user = db.get(token["userid"])
        if user is None:
            abort(400, "User Not Exists")
        user["pwdhash"] = gen_pwdhash(password)
        db.save(user)
        return "OK"

    def put_security(self, password, new_password, new_email):
        """修改账号信息"""
        if not check_password_hash(self.user["pwdhash"], password):
            abort(403, "Password Incorrect")
        self.user["email"] = new_email
        if new_password:
            self.user["pwdhash"] = gen_pwdhash(password)
        db.save(self.user)
        return self.user

    def put(self, repo, photo):
        """修改个人信息"""
        self.user["repo"] = repo
        self.user["photo"] = photo
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
                "article": {
                    "title": "error reason",
                    "date": "error reason",
                    ...
                },
                ...
            }
        </pre>
        """
        repo = self.user.get("repo")
        count = 0
        errors = {}
        if not repo:
            abort(400, "you didn't set your repo")
        for meta, content in util.read_repo(repo, "data"):
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
