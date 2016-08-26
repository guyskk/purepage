SECRET_KEY = "SECRET_KEY"
COUCHDB_DATABASE = "http://admin:123456@127.0.0.1:5984/purepage"
GITHUB_CLIENT_ID = "XXX"
GITHUB_CLIENT_SECRET = "YYY"
# 用于注册&找回密码
USER_AUTH_SECRET = "SECRET"
USER_AUTH_ALG = "HS256"
SERVER_URL = "127.0.0.1:5000"
# RATELIMIT_GLOBAL = ["2 per minute", "1 per second"]

# 邮件
MAIL_DEBUG = True
MAIL_USE_SSL = True
MAIL_PORT = 465
# [163]容易被识别为垃圾邮件
MAIL_SERVER = "smtp.163.com"
MAIL_USERNAME = "xxx@163.com"
MAIL_PASSWORD = "xxx"
MAIL_DEFAULT_SENDER = "xxx <xxx@163.com>"
# [QQ]较稳定
# MAIL_SERVER = "smtp.qq.com"
# MAIL_USERNAME = "xxx@qq.com"
# MAIL_PASSWORD = "xxx"
# MAIL_DEFAULT_SENDER = "xxx <xxx@qq.com>"
