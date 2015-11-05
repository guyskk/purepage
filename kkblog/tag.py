# coding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask.ext.restaction import Resource, abort, schema
from pony.orm import select, db_session, count
from kkblog import model
from kkblog import cache


class Tag(Resource):

    """文章标签"""
    name = "unicode&required", None, "标签名称"
    count = "int&required", None, "文章数量"
    schema_outputs = {
        "get_list": [schema("name", "count")]
    }

    def get_list(self):
        """获取所有标签"""
        with db_session:
            out_tag = lambda t: {"name": t.name, "count": count(t.article_metas)}
            tags = [out_tag(t) for t in model.Tag.select()]
            return tags
