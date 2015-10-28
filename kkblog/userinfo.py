# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import request, url_for
from flask.ext.restaction import Resource, abort
from pony.orm import select, db_session, count

from kkblog import model
from kkblog import user


def update_userinfo(id, **info):
    u = model.User.get(id=id)
    if u:
        u.userinfo.set(**info)
        return u
    else:
        return None


class UserInfo(Resource):

    """用户基本信息"""
    s_id = ("id", {
        "validate": "int",
        "required": True
    })
    s_username = ("username", {
        "validate": "email",
        "required": True
    })
    s_photo_url = ("photo_url", {"validate": "url"})
    s_nickname = ("nickname", {"validate": "unicode"})
    s_sex = ("sex", {"validate": "bool"})
    s_birthday = ("birthday", {"validate": "datetime"})

    s_email = ("email", {"validate": "email", })
    s_phone = ("phone", {"validate": "phone", })

    s_date_create = ("date_create", {"validate": "iso_datetime", })
    s_lastlogin_date = ("lastlogin_date", {"validate": "iso_datetime", })
    s_lastlogin_ip = ("lastlogin_ip", {"validate": "ipv4", })
    s_lastlogin_ua = ("lastlogin_ua", {"validate": "unicode", })

    s_birthday_out = ("birthday", {"validate": "iso_datetime"})

    s_info_public = dict([s_id, s_nickname, s_photo_url, s_sex, s_birthday_out])
    s_info_private = dict([s_email, s_phone, s_date_create,
                           s_lastlogin_date, s_lastlogin_ip, s_lastlogin_ua])
    s_info_all = dict(s_info_public, **s_info_private)

    s_info_in = dict([s_photo_url, s_nickname, s_sex, s_email, s_phone, s_birthday])

    s_message = ("message", {"validate": "unicode"})

    schema_inputs = {
        "get": dict([s_id]),
        "get_by_username": dict([s_username]),
        "get_me": None,
        "put": s_info_in,
    }
    schema_outputs = {
        "get": s_info_public,
        "get_by_username": s_info_public,
        "get_me": s_info_all,
        "put": s_info_all,
    }

    @staticmethod
    def user_role(user_id):
        return user.user_role(user_id)

    def get(self, id):
        """获取用户的公开信息"""
        with db_session:
            u = user.get_user_by_id(id)
            if u is None:
                abort(404)
            return u.userinfo.to_dict()

    def get_by_username(self, username):
        """获取用户的公开信息"""
        with db_session:
            u = model.User.get(username=username)
            if u is None:
                abort(404)
            return u.userinfo.to_dict()

    def get_me(self):
        """获取用户的个人信息"""
        id = request.me["id"]
        with db_session:
            u = user.get_user_by_id(id)
            if u is None:
                abort(404)
            return u.userinfo.to_dict()

    def put(self, **info):
        """修改个人信息"""
        id = request.me["id"]
        with db_session:
            u = update_userinfo(id, **info)
            if u is None:
                abort(404)
            return u.userinfo.to_dict()
