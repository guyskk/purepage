# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from flask import Flask, Blueprint
from werkzeug.local import LocalProxy
from flask_restaction import Api, Gen, Auth, Permission
from flask_github import GitHub
from .flask_couchdb import CouchDB

couch = CouchDB()
db = LocalProxy(lambda: couch.db)
github = GitHub()
api = Api()
auth = Auth()

from .webhooks import Webhooks
from .resource import Article, Comment, User
from .captcha import Captcha


def fn_user_role(token):
    if token and "userid" in token:
        user = db.get(token["userid"], None)
        if user is not None:
            return user["role"]
    return None


def create_app():
    app = Flask(__name__)
    app.config.from_object("config_default")

    app.route("/webhooks")(Webhooks())
    couch.init_app(app)
    github.init_app(app)

    bp_api = Blueprint('api', __name__, static_folder='static')
    api.init_app(app, blueprint=bp_api)
    api.add_resource(Article)
    api.add_resource(Comment)
    api.add_resource(User)
    api.add_resource(Captcha)
    api.add_resource(Permission, auth=auth)
    auth.init_api(api, fn_user_role=fn_user_role)
    app.register_blueprint(bp_api, url_prefix='/api')

    gen = Gen(api)
    gen.resjs()
    gen.resdocs()
    gen.permission()
    return app


def config_cors(app):
    # 跨域
    from flask_cors import CORS
    auth_header = app.config.get("API_AUTH_HEADER") or api.auth_header
    resources = {
        r"*": {"expose_headers": [auth_header]},
    }
    CORS(app, resources=resources)
