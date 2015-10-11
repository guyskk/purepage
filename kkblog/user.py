# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import request, url_for
from flask_restaction import Resource, abort

from validater import add_validater
from pony.orm import select, db_session, count

from datetime import datetime
from kkblog import model
from kkblog import api


def _out_user(u):
    if u:
        return dict(u.to_dict(), info=u.info.to_dict())
    else:
        return None


def _get_user(id):
    try:
        uid = int(id)
    except:
        return None
    with db_session:
        u = model.User.get(id=uid)
        return _out_user(u)


def _login_auth(user, password):
    if user is None:
        return False
    pwd = user.hashsalt + password
    return pwd == user.password


def _put_user(id, **info):
    with db_session:
        u = model.User.get(id=id)
        if u:
            u.info.set(info)
            return _out_user(u)
        else:
            return None


def add_admin(email, password):
    with db_session:
        u = model.User.get(username=email)
        role = "user.admin"
        if u:
            u.role = role
        else:
            hashsalt = "hashsalt"
            date_modify = datetime.now()
            pwd = hashsalt + password
            info = model.UserInfo(date_create=date_modify, email=email)
            u = model.User(username=email, password=pwd,
                           role=role, date_modify=date_modify,
                           hashsalt=hashsalt, info=info)


def abort_if_not_admin(msg):
    role = request.me["role"]
    if role != "user.admin":
        abort(403, msg)


class User(Resource):

    """docstring for User"""
    s_id = ("id", {
        "validate": "int",
        "required": True
    })
    s_username = ("username", {
        "validate": "re_email",
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
        "validate": "userrole",
        "required": True,
        "default": "user.normal"
    })
    s_email = ("email", {
        "validate": "re_email",
        "required": True
    })
    s_info_public = ("info", {
        "nickname": {"validate": "unicode", },
        "article_repo": {"validate": "re_url", },
        "website": {"validate": "re_url", },
        "sex": {"validate": "bool", },
        "birthday": {"validate": "iso_datetime", }
    })
    s_info_private = ("info", {
        "email": {"validate": "re_email", },
        "phone": {"validate": "re_phone", },
        "date_create": {"validate": "iso_datetime", },
        "lastlogin_date": {"validate": "iso_datetime", },
        "lastlogin_ip": {"validate": "re_ipv4", },
        "lastlogin_ua": {"validate": "unicode", },
    })
    s_info_all = ("info", dict(s_info_public[1], **s_info_private[1]))

    s_info_in = {
        "nickname": {"validate": "unicode", },
        "article_repo": {"validate": "re_url", },
        "website": {"validate": "re_url", },
        "sex": {"validate": "bool", },
        "birthday": {"validate": "datetime", },
        "email": {"validate": "re_email", },
        "phone": {"validate": "re_phone", },
    }
    s_token = ("token", {
        "validate": "unicode",
    })
    s_date_modify = ("date_modify", {"validate": "iso_datetime", })
    s_message = ("message", {"validate": "unicode"})
    s_out_public = dict([s_id, s_info_public])
    s_out_all = dict([s_id, s_role, s_username, s_date_modify, s_info_all])

    schema_inputs = {
        "get": dict([s_id]),
        "get_me": None,
        "post_register": dict([s_email, s_password, s_role]),
        "post_login": dict([s_username, s_password]),
        "post_logout": None,
        "post_fogot_password": dict([s_email]),
        "post_reset_password": dict([s_token, s_password]),
        "put": s_info_in,
        "put_password": dict([s_password, s_new_password]),
        "delete": None,
    }
    schema_outputs = {
        "get": s_out_public,
        "get_me": s_out_all,
        "post_register": s_out_public,
        "post_login": s_out_public,
        "post_logout": dict([s_message]),
        "post_fogot_password": dict([s_message]),
        "post_reset_password": dict([s_message]),
        "put": s_out_public,
        "put_password": dict([s_message]),
        "delete": dict([s_message]),
    }

    @staticmethod
    def user_role(user_id):
        if user_id is None:
            return "*"
        with db_session:
            u = model.User.get(id=user_id)
            if u:
                return u.role
            else:
                return "*"

    def get(self, id):
        """获取用户的公开信息"""
        u = _get_user(id)
        return u if u else abort(404)

    def get_me(self):
        """获取用户的个人信息"""
        id = request.me["id"]
        u = _get_user(id)
        return u if u else abort(404)

    def post_register(self, email, password, role="user.normal"):
        """注册，邮箱作为用户名"""
        if role != "user.normal":
            abort_if_not_admin("role can't be %s" % role)
        with db_session:
            u = model.User.get(username=email)
            if u:
                abort(400, "%s已注册" % email)
            hashsalt = "hashsalt"
            date_modify = datetime.now()
            pwd = hashsalt + password
            info = model.UserInfo(date_create=date_modify, email=email)
            u = model.User(username=email, password=pwd,
                           role=role, date_modify=date_modify,
                           hashsalt=hashsalt, info=info)

            return _out_user(u)

    def post_login(self, username, password):
        """登录"""
        with db_session:
            u = model.User.get(username=username)
            if _login_auth(u, password):
                me = {"id": u.id}
                header = api.gen_auth_header(me, auth_exp=3600)
                return _out_user(u), header
        abort(403)

    def post_logout(self):
        """退出登录"""
        return {"message": url_for("api.user@login")}

    def post_fogot_password(self, email):
        """忘记密码/申请重新设置密码"""
        with db_session:
            u = model.UserInfo.get(email=email)
            if u:
                token = "id+exp+modify_date+hash"
                # 发送邮件
                return {"message": "重置密码链接已发送到您的邮箱，请查看邮将"}
        abort(400)

    def post_reset_password(self, token, password):
        """重新设置密码"""
        id, exp, modify_date = token
        with db_session:
            u = model.User.get(id=id)
            if u and modify_date == u.modify_date:
                pwd = u.hashsalt + password
                u.password = pwd
                return {"message": url_for("api.user@login")}
        abort(400)

    def put_password(self, password, new_password):
        """修改密码"""
        id = request.me["id"]
        with db_session:
            u = model.User.get(id=id)
            if _login_auth(u, password):
                pwd = u.hashsalt + new_password
                u.password = pwd
                header = {api.auth_header: ""}
                return {"message": "success"}, header
        abort(403)

    def put(self, **info):
        """修改个人信息"""
        id = request.me["id"]
        u = _put_user(id, **info)
        return u if u else abort(404)

    def delete(self, password):
        """删除此账号"""
        id = request.me["id"]
        with db_session:
            u = model.User.get(id=id)
            if u:
                self.post_login(u.username, password)
                u.delete()
                return {"message": "success"}
            else:
                abort(404)

    # 以下功能仅限管理员使用

    def get_list(self):
        """获取所有用户信息"""
        with db_session:
            return [_out_user(u) for u in model.User.select()]
