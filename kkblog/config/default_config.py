# coding:utf-8

from __future__ import unicode_literals

DEBUG = True
SQL_DEBUG = False
# DEBUG_LEVEL = "INFO"
ALLOW_CORS = True
# TESTING = True

DATABASE_NAME = 'sqlite'
DATABASE_PATH = 'data/kkblog.db'
ARTICLE_DEST = "data/article_repo"
USER_AUTH_SECRET = "USER_AUTH_SECRET"
USER_ADMIN_EMAIL = "admin@admin.com"
USER_ADMIN_PASSWORD = "123456"
USER_ADMIN_REPO_URL = "https://github.com/guyskk/kkblog-article.git"

# CACHE_TYPE = "memcached"

API_PERMISSION_PATH = "permission.json"
API_AUTH_HEADER = "Authorization"
API_AUTH_TOKEN_NAME = "res_token"
API_AUTH_SECRET = "SECRET"
API_AUTH_ALG = "HS256"
API_AUTH_EXP = 1200
API_RESJS_NAME = "res.js"
API_RESDOCS_NAME = "resdocs.html"
API_BOOTSTRAP = "http://apps.bdimg.com/libs/bootstrap/3.3.4/css/bootstrap.css"
