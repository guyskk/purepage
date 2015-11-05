# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import request, url_for
from flask.ext.restaction import Resource, abort, schema
from pony.orm import select, db_session, count

from kkblog import model
from kkblog import user


@db_session
def update_userinfo(user_id, **info):
    user = model.User.get(id=user_id)
    if user is None:
        abort(404)
    userinfo = user.userinfo
    userinfo.set(**info)
    return dict(userinfo.to_dict(), user_id=user_id)


@db_session
def get_userinfo(user_id):
    user = model.User.get(id=user_id)
    if user is None:
        abort(404)
    info = user.userinfo
    return dict(info.to_dict(), user_id=user_id)


class UserInfo(Resource):

    """用户基本信息"""
    user_id = "int&required"
    username = "email&required"
    photo_url = "url"
    nickname = "unicode"
    sex = "bool", None, "True表示男,False表示女"

    email = "email"
    phone = "phone"

    date_create = "iso_datetime"
    lastlogin_date = "iso_datetime"
    lastlogin_ip = "ipv4"
    lastlogin_ua = "unicode"

    birthday = "iso_datetime"
    message = "unicode"

    public_items = ["user_id", "nickname", "photo_url", "sex", "birthday"]
    private_items = ["email", "phone", "date_create", "lastlogin_date",
                     "lastlogin_ip", "lastlogin_ua"]
    info_public = schema(*public_items)
    info_private = schema(*private_items)
    info_all = schema(*(public_items + private_items))

    info_in = schema("photo_url", "nickname", "sex", "email", "phone", "birthday")

    schema_inputs = {
        "get": schema("user_id"),
        "get_me": None,
        "put": info_in,
    }
    schema_outputs = {
        "get": info_public,
        "get_me": info_all,
        "put": info_all,
    }

    @staticmethod
    def user_role(user_id):
        return user.user_role(user_id)

    def get(self, id):
        """获取用户的公开信息"""
        return get_userinfo(id)

    def get_me(self):
        """获取用户的个人信息"""
        return get_userinfo(request.me["id"])

    def put(self, **info):
        """修改个人信息"""
        return update_userinfo(request.me["id"], **info)
