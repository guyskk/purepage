# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import request, url_for, current_app
from flask.ext.restaction import Resource, abort, schema
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from pony.orm import select, db_session, count
from kkblog import api, model, mail
from flask.ext.mail import Message


class InvalidTokenError(Exception):
    """reset_password token invalid"""


@db_session
def user_role(user_id):
    user = get_user_by_id(user_id)
    if user is not None:
        return user.role


@db_session
def add_admin(email, password):
    user = model.User.get(username=email)
    role = "user.admin"
    pwdhash = gen_pwdhash(password)
    now = datetime.now()
    user_config = {
        "date_modify": now,
        "role": role,
        "pwdhash": pwdhash,
    }
    info_config = {
        "date_create": now,
        "email": email,
    }
    if user:
        user.set(**user_config)
        user.userinfo.set(**info_config)
    else:
        user = model.User(username=email, **user_config)
        userinfo = model.UserInfo(user=user, **info_config)


def gen_pwdhash(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)


def add_user(email, password, role):
    user = model.User.get(username=email)
    if user is not None:
        raise ValueError("user %s already exists" % email)
    pwdhash = gen_pwdhash(password)
    now = datetime.now()
    user = model.User(username=email, pwdhash=pwdhash, date_modify=now, role=role)
    userinfo = model.UserInfo(user=user, date_create=now, email=email)
    return user


def login(username, password):
    user = model.User.get(username=username)
    if user is None:
        return False, None
    return check_password_hash(user.pwdhash, password), user


def change_password(username, new_password):
    user = model.User.get(username=username)
    if user is None:
        raise ValueError("user %s not exists" % username)
    pwdhash = gen_pwdhash(new_password)
    user.set(pwdhash=pwdhash, date_modify=datetime.now())
    return user


def reset_password(token, new_password):
    auth_secret = current_app.config["USER_AUTH_SECRET"]
    auth_alg = current_app.config["USER_AUTH_ALG"]
    options = {
        'require_exp': True,
    }
    try:
        tk = jwt.decode(token, auth_secret, algorithms=[auth_alg], options=options)
    except AttributeError as ex:
        raise InvalidTokenError("Invalid token: %s" % str(ex))
    except jwt.InvalidTokenError as ex:
        raise InvalidTokenError(str(ex))

    user = get_user_by_id(tk["id"])
    if user is None:
        raise ValueError("user id=%s not exists" % tk["id"])

    if user.date_modify.isoformat() != tk["date_modify"]:
        raise InvalidTokenError("The token is invalid")

    pwdhash = gen_pwdhash(new_password)
    user.set(pwdhash=pwdhash, date_modify=datetime.now())
    return user


def forgot_password(username):
    auth_secret = current_app.config["USER_AUTH_SECRET"]
    auth_alg = current_app.config["USER_AUTH_ALG"]
    auth_exp = current_app.config["USER_AUTH_EXP"]
    user = model.User.get(username=username)
    if user is None:
        raise ValueError("user %s not exists" % username)
    exp = datetime.utcnow() + timedelta(seconds=auth_exp)
    token = {
        "id": user.id,
        "exp": exp,
        "date_modify": user.date_modify.isoformat(),
    }
    return jwt.encode(token, auth_secret, algorithm=auth_alg), user


def get_user_by_id(id):
    try:
        uid = int(id)
        return model.User.get(id=uid)
    except:
        return None


def get_auth_exp(remember_me=False):
    if remember_me:
        return current_app.config["USER_REMEMBER_ME_EXP"]
    else:
        return current_app.config["USER_LOGIN_EXP"]


class User(Resource):

    """docstring for User"""

    id = "int&required"
    username = "email&required"
    password = "password&required"
    new_password = "password&required"
    role = "role_user&required", "user.normal"
    email = "email&required"
    date_modify = "iso_datetime&required"
    token = "unicode&required"
    remember_me = "bool", False
    message = "unicode"

    schema_inputs = {
        "get": schema("id"),
        "get_me": None,
        "post_register": schema("email", "password"),
        "post_admin_register": schema("email", "password", "role"),
        "post_login": schema("username", "password", "remember_me"),
        "post_forgot_password": schema("username"),
        "post_reset_password": schema("token", "password"),
        "put_password": schema("password", "new_password"),
        "delete": None,
    }
    out = schema("id", "username", "role", "date_modify")
    schema_outputs = {
        "get": out,
        "get_me": out,
        "post_register": out,
        "post_admin_register": out,
        "post_login": out,
        "post_forgot_password": schema("message"),
        "post_reset_password": out,
        "put_password": out,
        "delete": schema("message"),
    }

    @staticmethod
    def user_role(user_id):
        return user_role(user_id)

    def get(self, id):
        """获取用户的信息"""
        with db_session:
            user = get_user_by_id(id)
            if user is None:
                abort(404)
            return user.to_dict()

    def get_me(self):
        """获取用户的个人信息，调用此接口可以延长token过期时间"""
        me = dict(request.me)
        auth_exp = get_auth_exp(me.get("remember_me"))
        header = api.gen_auth_header(me, auth_exp=auth_exp)
        return self.get(me["id"]), header

    def post_register(self, email, password):
        """注册，邮箱作为用户名"""
        return self.post_admin_register(email, password, role="user.normal")

    def post_admin_register(self, email, password, role):
        """注册，邮箱作为用户名，限管理员使用"""
        with db_session:
            try:
                user = add_user(email, password, role)
                return user.to_dict()
            except ValueError as ex:
                abort(400, str(ex))

    def post_login(self, username, password, remember_me):
        """登录"""
        with db_session:
            ok, user = login(username, password)
            if ok:
                me = {
                    "id": user.id,
                    "remember_me": remember_me
                }
                auth_exp = get_auth_exp(remember_me)
                header = api.gen_auth_header(me, auth_exp=auth_exp)
                return user.to_dict(), header
            else:
                abort(403, "用户名或密码错误")

    def post_forgot_password(self, username):
        """忘记密码/申请重新设置密码"""
        with db_session:
            try:
                token, user = forgot_password(username)
                email = user.userinfo.email
            except ValueError as ex:
                abort(400, str(ex))

        # 发送邮件
        tmpl = """
        <p><b>亲爱的{username}，你好，</b></p>
        <p>重置密码链接如下：</p>
        <a href="{link}">{link}</a>
        <p>请在30分钟内点击此链接，并进入下一步重新设置密码。</p>
        <p>如果你并未发出此请求，请忽略此邮件，无需采取进一步操作。</p>
        <p>本邮件由 <a href="http://www.kkblog.me">http://www.kkblog.me</a>
        发送，请勿直接回复。</p>
        """
        msg = Message("重新设置密码", recipients=[email])
        link = "%s?token=%s" % ("/reset_password", token)
        html = tmpl.format(username=username, link=link)
        msg.html = html
        mail.send(msg)
        current_app.logger.info("Send Mail:\n" + html)
        return {"message": "重置密码链接已发送到您的邮箱，请查看邮件"}

    def post_reset_password(self, token, password):
        """重新设置密码"""
        with db_session:
            try:
                user = reset_password(token, password)
                return user.to_dict()
            except (InvalidTokenError, ValueError) as ex:
                abort(400, str(ex))

    def put_password(self, password, new_password):
        """修改密码"""
        with db_session:
            user = get_user_by_id(request.me["id"])
            if user is None:
                abort(404)
            ok, user = login(user.username, password)
            if ok:
                change_password(user.username, new_password)
                return user.to_dict()
            else:
                abort(403)

    def delete(self, password):
        """删除此账号"""
        with db_session:
            user = get_user_by_id(request.me["id"])
            if user is None:
                abort(404)
            ok, user = login(user.username, password)
            if ok:
                user.delete()
                return {"message": "success"}
            else:
                abort(403)
