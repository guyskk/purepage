from time import time
DEBUG = True
MAIL_SUPPRESS_SEND = True
# use unique db for each test, avoid data not deleted after test
n = int(time() * 1000000)
COUCHDB_DATABASE = "http://admin:123456@127.0.0.1:5984/purepage-test%d" % n
