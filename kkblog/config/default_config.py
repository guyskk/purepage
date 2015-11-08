# coding:utf-8

from __future__ import unicode_literals

DEBUG = True
SQL_DEBUG = True
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

# 用于找回密码功能处理token
USER_AUTH_SECRET = "USER_AUTH_SECRET"
USER_AUTH_ALG = "HS256"
# 找回密码token过期时间，30分钟
USER_AUTH_EXP = 30 * 60
# 登录token过期时间，60分钟
USER_LOGIN_EXP = 60 * 60
# 记住我token过期时间，7天
USER_REMEMBER_ME_EXP = 7 * 24 * 60 * 60

API_AUTH_SECRET = "API_AUTH_SECRET"
API_PERMISSION_PATH = "config/permission.json"
API_BOOTSTRAP = "/static/css/bootstrap.min.css"

# 图形验证码加密密钥, must be either 16, 24, or 32 bytes long
CAPTCHA_KEY = "CAPTCHA_CAPTCHA_"
# 图形验证码加密盐过期时间，30分钟
CAPTCHA_SALT_EXP = 30 * 60
CAPTCHA_FONT = "georgia.ttf"
USER_ADMIN_EMAIL = "admin@admin.com"
USER_ADMIN_PASSWORD = "123456"
USER_ADMIN_REPO_URL = "https://github.com/guyskk/kkblog-article.git"

CACHE_TYPE = "simple"

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 25
MAIL_USERNAME = "KkBloG"
MAIL_DEFAULT_SENDER = None
MAIL_PASSWORD = None
