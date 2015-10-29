# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import request, url_for, current_app
from flask.ext.restaction import Resource, abort
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


def gen_pwdhash(password):
    return generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)


def add_user(username, password, role, email):
    pwdhash = gen_pwdhash(password)
    date_modify = datetime.now()
    user = model.User.get(username=username)
    if user is not None:
        raise ValueError("user %s already exists" % username)
    uinfo = model.UserInfo(user=user, date_create=date_modify, email=email)
    user = model.User(userinfo=uinfo, username=username, pwdhash=pwdhash,
                      date_modify=date_modify, role=role)
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


def reset_password(token, new_password, auth_secret, auth_alg="HS256"):
    options = {
        'require_exp': True,
    }
    try:
        tk = jwt.decode(token, auth_secret, algorithms=[auth_alg], options=options)
    except AttributeError as ex:
        raise InvalidTokenError("Invalid token: %s" % str(ex))
    except jwt.InvalidTokenError as ex:
        raise InvalidTokenError(str(ex))

    user = model.User.get(id=tk["id"])
    if user is None:
        raise ValueError("user id=%s not exists" % tk["id"])

    if user.date_modify.isoformat() != tk["date_modify"]:
        raise InvalidTokenError("password has been changed yet, this token is invalid")

    pwdhash = gen_pwdhash(new_password)
    user.set(pwdhash=pwdhash, date_modify=datetime.now())
    return user


def forgot_password(username, auth_secret, auth_alg="HS256", auth_exp=1800):
    user = model.User.get(username=username)
    if user is None:
        raise ValueError("user %s not registered" % username)
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
        # 一周内不用重新登录
        auth_exp = 7 * 24 * 60 * 60
    else:
        # 60分钟内不用重新登录
        auth_exp = 60 * 60
    return auth_exp


@db_session
def add_admin(email, password):
    user = model.User.get(username=email)
    role = "user.admin"
    pwdhash = gen_pwdhash(password)
    date_modify = datetime.now()
    user_config = {
        "date_modify": date_modify,
        "role": role,
        "pwdhash": pwdhash,
    }
    info_config = {
        "date_create": date_modify,
        "email": email,
    }
    if user:
        user.userinfo.set(**info_config)
        user.set(**user_config)
    else:
        info = model.UserInfo(**info_config)
        user = model.User(username=email, userinfo=info, **user_config)


class User(Resource):

    """docstring for User"""
    s_id = ("id", {
        "validate": "int",
        "required": True
    })
    s_username = ("username", {
        "validate": "email",
        "required": True
    })
    s_password = ("password", {
        "validate": "password",
        "required": True
    })
    s_new_password = ("new_password", {
        "validate": "password",
        "required": True
    })
    s_role = ("role", {
        "validate": "role_user",
        "required": True,
        "default": "user.normal"
    })
    s_email = ("email", {
        "validate": "email",
        "required": True
    })
    s_date_modify = ("date_modify", {
        "validate": "iso_datetime",
        "required": True
    })
    s_token = ("token", {
        "validate": "unicode",
        "required": True
    })
    s_remember_me = ("remember_me", {
        "validate": "bool",
        "default": False
    })
    s_message = ("message", {"validate": "unicode"})

    schema_inputs = {
        "get": dict([s_id]),
        "get_me": None,
        "post_register": dict([s_email, s_password]),
        "post_admin_register": dict([s_email, s_password, s_role]),
        "post_login": dict([s_username, s_password, s_remember_me]),
        "post_logout": None,
        "post_forgot_password": dict([s_username]),
        "post_reset_password": dict([s_token, s_password]),
        "put_password": dict([s_password, s_new_password]),
        "delete": None,
    }
    s_out = dict([s_id, s_username, s_role, s_date_modify])
    schema_outputs = {
        "get": s_out,
        "get_me": s_out,
        "post_register": s_out,
        "post_admin_register": s_out,
        "post_login": s_out,
        "post_logout": dict([s_message]),
        "post_forgot_password": dict([s_message]),
        "post_reset_password": s_out,
        "put_password": s_out,
        "delete": dict([s_message]),
    }

    def __init__(self):
        self.auth_secret = current_app.config["USER_AUTH_SECRET"]

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
        """获取用户的个人信息"""
        id = request.me["id"]
        me = {"id": id}
        header = api.gen_auth_header(me, auth_exp=get_auth_exp())
        return self.get(id), header

    def post_register(self, email, password):
        """注册，邮箱作为用户名"""
        return self.post_admin_register(email, password, role="user.normal")

    def post_admin_register(self, email, password, role):
        """注册，邮箱作为用户名，限管理员使用"""
        with db_session:
            try:
                user = add_user(email, password, role, email)
                return user.to_dict()
            except ValueError as ex:
                abort(400, str(ex))

    def post_login(self, username, password, remember_me):
        """登录"""
        with db_session:
            ok, user = login(username, password)
            if ok:
                me = {"id": user.id}
                header = api.gen_auth_header(me, auth_exp=get_auth_exp(remember_me))
                return user.to_dict(), header
            else:
                abort(403)

    def post_logout(self):
        """退出登录"""
        # s = unicode(url_for("api.user@login"))
        return {"message": "退出登录成功"}

    def post_forgot_password(self, username):
        """忘记密码/申请重新设置密码"""
        with db_session:
            try:
                token, user = forgot_password(username, auth_secret=self.auth_secret)
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
                user = reset_password(token, password, auth_secret=self.auth_secret)
                return user.to_dict()
            except (InvalidTokenError, ValueError) as ex:
                abort(400, str(ex))

    def put_password(self, password, new_password):
        """修改密码"""
        id = request.me["id"]
        with db_session:
            user = get_user_by_id(id)
            if user is None:
                abort(404)
            ok, user = login(user.username, password)
            if ok:
                change_password(user.username, new_password)
                header = {api.auth_header: ""}
                return user.to_dict(), header
            else:
                abort(403)

    def delete(self, password):
        """删除此账号"""
        id = request.me["id"]
        with db_session:
            user = get_user_by_id(id)
            if user is None:
                abort(404)
            ok, user = login(user.username, password)
            if ok:
                user.delete()
                return {"message": "success"}
            else:
                abort(403)
