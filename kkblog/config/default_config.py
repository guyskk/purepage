# coding:utf-8

from __future__ import unicode_literals

DEBUG = True
SQL_DEBUG = False
DEBUG_LEVEL = None  # "INFO"
ALLOW_CORS = True
MAIL_DEBUG = True
DEBUG_LOG = "data/kkblog_debug.log"
ERROR_LOG = "data/kkblog_error.log"

# don't set SERVER_NAME, it will cause all page 404
# SERVER_NAME = "127.0.0.1:5000"

DATABASE_NAME = 'sqlite'
DATABASE_PARAMS = {
    "filename": 'data/kkblog.db',
}

ARTICLE_DEST = "data/article_repo"
USER_AUTH_SECRET = "USER_AUTH_SECRET"

API_PERMISSION_PATH = "config/permission.json"
API_AUTH_SECRET = "API_AUTH_SECRET"
API_BOOTSTRAP = "/static/lib/bootstrap.css"

USER_ADMIN_EMAIL = "admin@admin.com"
USER_ADMIN_PASSWORD = "123456"
USER_ADMIN_REPO_URL = "https://github.com/guyskk/kkblog-article.git"

CACHE_TYPE = "simple"

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 25
MAIL_USERNAME = "KkBloG"
MAIL_DEFAULT_SENDER = None
MAIL_PASSWORD = None
