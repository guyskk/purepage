# coding:utf-8

from __future__ import unicode_literals
from pony.orm import *
from kkblog import db
from datetime import datetime


class BlogUser(db.Entity):
    date_create = Required(datetime)

    user_system = Required(unicode)
    user_id = Required(unicode)
    composite_key(user_system, user_id)

    git_username = Required(unicode, unique=True)
    role = Required(unicode)
    article_repo = Optional(unicode)
    latest_commit = Optional(unicode)
    website = Optional(unicode)
    article_metas = Set("ArticleMeta")
    comments = Set("Comment")
