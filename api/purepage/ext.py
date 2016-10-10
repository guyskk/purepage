import rethinkdb as r  # noqa
from flask import g  # noqa
from flask_restaction import abort  # noqa
from werkzeug.local import LocalProxy
from flask_github import GitHub
from flask_mail import Mail
from flask_limiter import Limiter
from flask_restaction import Api, TokenAuth
from flask_rethinkdb import Rethinkdb


class Dependency:

    def __init__(self, cls):
        self.cls = cls

    def init(self, *args, **kwargs):
        self.dependency = self.cls(*args, **kwargs)
        return self.dependency

    def __call__(self):
        try:
            return self.dependency
        except AttributeError:
            raise ValueError("%s not inited" % self.cls.__name__)

    def __iter__(self):
        return iter([LocalProxy(self), self.init])


api, init_api = Dependency(Api)
auth, init_auth = Dependency(TokenAuth)
mail, init_mail = Dependency(Mail)
github, init_github = Dependency(GitHub)
limiter, init_limiter = Dependency(Limiter)
db, init_db = Dependency(Rethinkdb)
