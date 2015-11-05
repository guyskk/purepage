# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from pony.orm import *
from kkblog import db
from datetime import datetime


class BlogUser(db.Entity):
    """博客主人"""
    # 绑定到User
    user_id = PrimaryKey(int)
    gitname = Required(unicode, unique=True)
    role = Required(unicode)
    date_create = Required(datetime)
    date_modify = Required(datetime)
    article_repo = Optional(unicode)
    latest_commit = Optional(unicode)
    articles = Set("Article")
    comments = Set("Comment")


class Article(db.Entity):
    """gitname, subdir, filename 唯一确定一篇文章"""
    gitname = Required(unicode)
    subdir = Required(unicode)
    filename = Required(unicode)
    composite_key(gitname, subdir, filename)

    bloguser = Optional("BlogUser")
    comments = Set("Comment")
    content = Optional("ArticleContent", cascade_delete=True)
    tags = Set("Tag")

    title = Required(unicode)
    subtitle = Optional(unicode)
    author = Optional(unicode)
    date_create = Required(datetime)
    date_modify = Required(datetime)


class ArticleContent(db.Entity):
    """文章内容和目录"""
    article = Required("Article")
    html = Required(LongUnicode)
    toc = Required(LongUnicode)


class Tag(db.Entity):
    article = Set("Article")
    name = Required(unicode)


class Comment(db.Entity):
    """评论"""

    # 唯一确定属于哪篇文章
    gitname = Required(unicode)
    subdir = Required(unicode)
    filename = Required(unicode)
    composite_index(gitname, subdir, filename)

    # 评论者
    user_id = Optional(int)
    # 所属文章,可能被删除
    article = Optional("Article")
    # 所属博客主人
    bloguser = Optional("BlogUser")

    content = Required(unicode)
    date_create = Required(datetime)
    date_modify = Required(datetime)
