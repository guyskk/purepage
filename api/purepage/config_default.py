# flask
DEBUG = True
SECRET_KEY = "SECRET_KEY"

# purepage
USER_AUTH_SECRET = "SECRET"
USER_AUTH_ALG = "HS256"
SERVER_URL = "127.0.0.1:5000"

# database
DATABASE = ""

# flask-limiter
RATELIMIT_GLOBAL = "50 per hour"

# github webhooks
GITHUB_CLIENT_ID = "XXX"
GITHUB_CLIENT_SECRET = "YYY"

# flask-mail
MAIL_DEBUG = True
MAIL_USE_SSL = True
MAIL_PORT = 465
# 163容易被识别为垃圾邮件, QQ较稳定
MAIL_SERVER = "smtp.163.com"
MAIL_USERNAME = "xxx@163.com"
MAIL_PASSWORD = "xxx"
MAIL_DEFAULT_SENDER = "xxx <xxx@163.com>"
