# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from pony.orm import *
from kkblog import db
from datetime import datetime


class User(db.Entity):
    """只包含必要信息"""
    username = Required(unicode, unique=True)
    pwdhash = Required(unicode)
    date_modify = Required(datetime)
    role = Required(unicode)
    userinfo = Optional("UserInfo", cascade_delete=True)


class UserInfo(db.Entity):
    """用户信息"""
    user = Required("User")
    email = Optional(unicode)
    nickname = Optional(unicode)
    birthday = Optional(datetime)
    # True 男/False 女
    sex = Optional(bool)
    phone = Optional(unicode)
    photo_url = Optional(unicode)

    date_create = Required(datetime)
    lastlogin_date = Optional(datetime)
    lastlogin_ip = Optional(unicode)
    lastlogin_ua = Optional(unicode)
