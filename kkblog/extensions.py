# coding:utf-8

from __future__ import absolute_import

from flask.ext.restaction import Api
from pony.orm import Database
from flask.ext.cache import Cache
from flask.ext.mail import Mail

__all__ = ['api', 'db', 'cache', 'mail']
api = Api()
db = Database()
cache = Cache()
mail = Mail()
