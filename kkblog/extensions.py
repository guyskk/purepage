# coding:utf-8

from __future__ import unicode_literals

from flask_restaction import Api
from pony.orm import Database

__all__ = ['api', 'db']
api = Api()
db = Database()
