# coding:utf-8

from __future__ import unicode_literals
from pony.orm import *
from kkblog import db
from datetime import datetime


class User(db.Entity):

    username = Required(unicode, unique=True)
    password = Required(unicode)
    hashsalt = Required(unicode)
    date_modify = Required(datetime)
    role = Required(unicode)
    info = Required("UserInfo")


class UserInfo(db.Entity):

    user = Optional("User")
    date_create = Required(datetime)
    email = Optional(unicode)
    nickname = Optional(unicode)
    birthday = Optional(datetime)
    # True 男/False 女
    sex = Optional(bool)
    phone = Optional(unicode)
    lastlogin_date = Optional(datetime)
    lastlogin_ip = Optional(unicode)
    lastlogin_ua = Optional(unicode)
    photo_url = Optional(unicode)
