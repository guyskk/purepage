"""flask exts"""
from flask_restaction import Api, Auth
from flask_github import GitHub
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_couchdb import CouchDB

db = CouchDB()
github = GitHub()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
api = Api()
auth = Auth()
