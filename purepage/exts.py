"""flask exts"""
from werkzeug.local import LocalProxy
from flask_restaction import Api, Auth
from flask_github import GitHub
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from kkblog.flask_couchdb import CouchDB

couch = CouchDB()
db = LocalProxy(lambda: couch.db)
github = GitHub()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
api = Api()
auth = Auth()
