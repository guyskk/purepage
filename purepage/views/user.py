"""User API"""
import jwt
from datetime import datetime, timedelta
from flask import request, abort, g, current_app, render_template
from json import JSONDecodeError
from flask_restaction import Resource, Res
from werkzeug.security import generate_password_hash, check_password_hash
from couchdb.http import Conflict, NotFound
from purepage import auth, api, db, util


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
        raise InvalidTokenError("Invalid token: %s" % str(ex))
    except jwt.InvalidTokenError as ex:
        raise InvalidTokenError("Invalid token: %s" % str(ex))
    return tk


def encode_token(token, exp=1800):
    """编码json web token"""
    auth_secret = current_app.config["USER_AUTH_SECRET"]
    auth_alg = current_app.config["USER_AUTH_ALG"]
    token['exp'] = datetime.utcnow() + timedelta(seconds=exp)
    token = jwt.encode(token, auth_secret, algorithm=auth_alg)
    return token.decode('utf-8')


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
        "photo": ("unicode&default='/static/image/photo-default.png'", "头像"),
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

    def get(self, userid):
        """获取用户信息"""
        user = db.get(userid)
        return user

    def get_me(self):
        """获取自己的信息"""
        return g.user

    def post_verify(self, userid, email):
        """验证用户名和邮箱"""
        token = {
            "type": "signup",
            "userid": userid,
            "email": email
        }
        if userid in db:
            abort(400, "UserID Already SignUp")
        if db.count(('user', 'email'), key=email) >= 1:
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
        try:
            token = decode_token(token)
        except InvalidTokenError as ex:
            abort(400, str(ex))
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
            user = db.put(user)
        except Conflict:
            abort(400, "UserID Conflict")
        # check after save
        if db.count(('user', 'email'), key=token["email"]) > 1:
            db.delete(user)
            abort(400, "Email Already SignUp")
        headers = auth.gen_header({"userid": token['userid']})
        return "OK", 201, headers

    def post_login(self, userid, password, expiration):
        """登录"""
        try:
            user = db.get(userid)
        except NotFound:
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
        result = db.query("user/by_email", **params)
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
        try:
            token = decode_token(token)
        except InvalidTokenError as ex:
            abort(403, str(ex))
        if token["type"] != "reset":
            abort(400, "Token Type Incorrect")
        user = db.get(token["userid"])
        if user is None:
            abort(400, "User Not Exists")
        user["pwdhash"] = gen_pwdhash(password)
        db.put(user)
        return "OK"

    def put_security(self, password, new_password, new_email):
        """修改账号信息"""
        if not check_password_hash(self.user["pwdhash"], password):
            abort(403, "Password Incorrect")
        g.user["email"] = new_email
        if new_password:
            g.user["pwdhash"] = gen_pwdhash(password)
        db.put(g.user)
        return g.user

    def put(self, repo, photo):
        """修改个人信息"""
        g.user["repo"] = repo
        g.user["photo"] = photo
        db.put(g.user)
        return g.user

    def post_sync_repo(self):
        """同步博客仓库

        需要先设置好自己的博客仓库地址（调用修改个人信息接口）。
        服务器会从仓库下载所有文件，并解析其中的 markdown 文件。
        再将解析后的文章内容和标题，日期等信息保存到数据库中。
        """
        res = Res(api, headers=request.headers)
        repo = g.user["repo"]
        count = 0
        errors = {}
        if not repo:
            abort(400, "you didn't set your repo")
        for meta, content in util.read_repo(repo, "data"):
            meta["content"] = content
            meta['date'] = util.format_date(meta['date'])
            resp = res.article.post(meta)
            if resp.status_code != 200:
                try:
                    errors[meta["title"]] = resp.json
                except JSONDecodeError:
                    errors[meta["title"]] == resp.data
            else:
                count += 1
        return {
            "succeed": count,
            "errors": errors
        }
