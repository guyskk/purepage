# coding:utf-8

from __future__ import unicode_literals
from pony.orm import *
from . import db


class Article(db.Entity):
    content = Required(unicode)
    toc = Required(unicode)
    meta = Required("ArticleMeta")


class ArticleMeta(db.Entity):
    article = Optional("Article")
    title = Required(unicode)
    subtitle = Optional(unicode)
    tags = Set("Tag")
    date = Required(unicode)
    author = Optional(unicode)


class Tag(db.Entity):
    article_meta = Optional("ArticleMeta")
    name = Required(unicode)


class User(db.Entity):
    username = Required(unicode)
    password = Required(unicode)
    role = Required(unicode)
