"""User API"""
import arrow
from flask import render_template, request
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from purepage.ext import r, db, abort, g, auth, mail


def gen_pwdhash(password):
    """生成密码hash"""
    return generate_password_hash(password, method='pbkdf2:sha256')


class User:
    """
    用户

    $shared:
        user:
            id?str: 用户ID
            role?str: 角色
            github?url&optional: Github地址
            avatar?url&default="http://purepage.org/static/avatar-default.png": 头像
            date_create?datetime&optional: 创建时间
            date_modify?datetime&optional: 修改时间
            lastlogin_date?datetime&optional: 最近登录时间
    """  # noqa

    def post_signup(self, id, email, password):
        """
        注册

        $input:
            id?str: 用户ID
            email?email&optional: 邮箱
            password?str: 密码
        $output: @message
        $error:
            400.IDConflict: 用户ID已存在
            400.EmailConflict: 邮箱已存在
        """
        if db.run(r.table("user").get(id)):
            abort(400, "IDConflict", "%s already exists" % id)
        if email and db.first(r.table("user").filter({"email": email})):
            abort(400, "EmailConflict", "%s already exists" % email)
        db.run(r.table("user").insert({
            "id": id,
            "email": email,
            "pwdhash": gen_pwdhash(password),
            "role": "normal",
            "date_create": arrow.utcnow().datetime,
            "date_modify": arrow.utcnow().datetime,
            "timestamp": arrow.utcnow().timestamp
        }))
        return {"message": "OK"}

    def check_password(self, user, password):
        if not user:
            abort(403, "UserNotFound", "帐号不存在")
        if not check_password_hash(user["pwdhash"], password):
            abort(403, "WrongPassword", "密码错误")

    def post_login(self, account, password):
        """
        登录

        $input:
            account?str: 用户ID或邮箱
            password?str: 密码
        $output: @user
        $error:
            403.UserNotFound: 帐号不存在
            403.WrongPassword: 密码错误
        """
        user = db.run(r.table("user").get(account))
        if not user:
            user = db.first(r.table("user").filter({"email": account}))
        if not user:
            abort(403, "UserNotFound", "帐号不存在")
        self.check_password(user, password)
        db.run(
            r.table("user")
            .get(user["id"])
            .update({
                "lastlogin_date": arrow.utcnow().datetime,
                "lastlogin_ip": request.remote_addr,
                "lastlogin_ua": request.headers.get('User-Agent'),
                "timestamp": arrow.utcnow().timestamp
            })
        )
        g.token = {"type": "login", "id": user["id"]}
        return user

    def get_me(self):
        """
        获取自己的信息

        $output: @user
        """
        return g.user

    def get(self, id):
        """
        查看用户信息

        $input:
            id?str: ID
        $output: @user
        """
        user = db.run(r.table("user").get(id))
        if not user:
            abort(404, "NotFound", "用户不存在")
        return user

    def put(self, github, avatar):
        """
        修改个人信息

        $input:
            github?url&optional: Github地址
            avatar?url&optional: 头像
        $output: @message
        """
        db.run(
            r.table("user")
            .get(g.user["id"])
            .update({
                "github": github,
                "avatar": avatar,
                "date_modify": arrow.utcnow().datetime,
                "timestamp": arrow.utcnow().timestamp
            })
        )
        return {"message": "OK"}

    def put_email(self, email, password):
        """
        修改邮箱地址

        $input:
            email?email: 邮箱
            password?str: 密码
        $output: @message
        """
        self.check_password(g.user, password)
        db.run(r.table("user").get(g.user["id"]).update({
            "email": email,
            "date_modify": arrow.utcnow().datetime,
            "timestamp": arrow.utcnow().timestamp
        }))
        return {"message": "OK"}

    def put_password(self, new_password, password):
        """
        修改密码

        $input:
            new_password?str: 新密码
            password?str: 密码
        $output: @message
        """
        self.check_password(g.user, password)
        db.run(r.table("user").get(g.user["id"]).update({
            "pwdhash": gen_pwdhash(new_password),
            "date_modify": arrow.utcnow().datetime,
            "timestamp": arrow.utcnow().timestamp
        }))
        return {"message": "OK"}

    def post_forgot(self, email):
        """
        忘记密码，Token有效时间为2小时

        $input:
            email?email: 邮箱
        $output: @message
        $error:
            400.UserNotFound: 用户不存在
        """
        user = db.first(r.table("user").filter(r.row["email"] == email))
        if not user:
            abort(400, "UserNotFound", "用户不存在")
        token = auth.encode_token({
            "type": "reset",
            "id": user["id"],
            "exp": arrow.utcnow().replace(hours=2).timestamp,
            "timestamp": user["timestamp"]
        })
        token = token.decode("ascii")
        msg = Message("PurePage重置密码", recipients=[email])
        msg.html = render_template(
            "user-reset.html", token=token, userid=user["id"])
        mail.send(msg)
        return {"message": "重置链接已发送至邮箱，请查收"}

    def post_reset(self, token, password):
        """
        重置密码

        $input:
            token?str: 重置链接中的Token
            password?str: 密码
        $output: @message
        $error:
            403.InvalidToken: Token无效
        """
        token = auth.decode_token(token)
        if token is None or token.get("type") != "reset":
            abort(403, "InvalidToken", "Token无效")
        user = db.run(r.table("user").get(token["id"]))
        if (
            user is None
            or "timestamp" not in token
            or user["timestamp"] != token["timestamp"]
        ):
            abort(403, "InvalidToken", "Token无效")
        db.run(
            r.table("user")
            .get(token["id"])
            .update({
                "pwdhash": gen_pwdhash(password),
                "timestamp": arrow.utcnow().timestamp
            })
        )
        return {"message": "OK"}
