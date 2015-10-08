# coding:utf-8

from __future__ import unicode_literals
from pony.orm import *
from kkblog import db
from datetime import datetime


class BlogUser(db.Entity):
    date_create = Required(datetime)
    user_system = Required(unicode)
    user_id = Required(unicode)
    role = Required(unicode)
    article_repo = Optional(unicode)
    git_username = Required(unicode, unique=True)
    latest_commit = Optional(unicode)
    website = Optional(unicode)
    article_metas = Set("ArticleMeta")
    comments = Set("Comment")
