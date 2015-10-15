# coding:utf-8

from __future__ import unicode_literals
from pony.orm import *
from kkblog import db
from datetime import datetime


class Article(db.Entity):

    content = Required(LongUnicode)
    toc = Required(LongUnicode)
    meta = Required("ArticleMeta")


class ArticleMeta(db.Entity):
    article = Optional("Article")

    bloguser = Required("BlogUser")
    subdir = Required(unicode)
    filename = Required(unicode)
    composite_key(bloguser, subdir, filename)

    title = Required(unicode)
    subtitle = Optional(unicode)
    tags = Set("Tag")
    date_create = Required(datetime)
    date_modify = Required(datetime)
    author = Optional(unicode)

    def get_comments(self):
        return select(c for c in Comment if c.article_subdir == self.subdir
                      and c.article_filename == self.filename)


class Tag(db.Entity):
    article_metas = Set("ArticleMeta")
    name = Required(unicode)


class Comment(db.Entity):

    """评论"""
    article_bloguser = Required("BlogUser")
    article_subdir = Required(unicode)
    article_filename = Required(unicode)
    composite_key(article_bloguser, article_subdir, article_filename)

    content = Required(unicode)
    date = Required(datetime)
    nickname = Required(unicode)
    photo_url = Optional(unicode)
    email = Optional(unicode)
