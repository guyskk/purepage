from purepage import create_app, api, auth, db
from purepage import util
from purepage.views import user
from flask_restaction import Res
import pytest
import logging

logging.basicConfig(level=logging.DEBUG)

now = util.now()
pwdhash = user.gen_pwdhash('123456')
user = {
    "type": "user",
    "_id": "guyskk",
    "email": "guyskk@qq.com",
    "pwdhash": pwdhash,
    "date_create": now,
    "date_modify": now,
    "role": "normal",
    "photo": "http://www.purepage.org/logo.png",
    "repo": "https://github.com/guyskk/purepage-article.git"
}

article1 = {
    "type": "article",
    "_id": "guyskk.2016.hello",
    "userid": "guyskk",
    "catalog": "2016",
    "article": "hello",
    "date": now,
    "title": "hello world",
    "tags": ["python", "purepage"],
    "summary": "first article in 2016",
    "content": "2016",
}

article2 = {
    "type": "article",
    "_id": "xxx.2015.hello",
    "userid": "xxx",
    "catalog": "2015",
    "article": "hello",
    "date": now,
    "title": "hello world",
    "tags": ["javascript", "purepage"],
    "summary": "first article in 2015",
    "content": "2015",
}
comment = {
    "type": "comment",
    "_id": "guyskk.2016.hello.%s.guyskk" % now,
    "article": "guyskk.2016.hello",
    "userid": "guyskk",
    "date": now,
    "content": "good"
}


@pytest.yield_fixture(scope="session")
def app():
    app = create_app("purepage.config_test")
    db.load_designs("design")
    data = [user, article1, article2, comment]
    db.bulk_docs(data)
    yield app
    db.destroy()


@pytest.fixture(scope="session")
def guest(app):
    return Res(api)


@pytest.fixture(scope="function")
def res(app):
    headers = auth.gen_header({"userid": 'guyskk'}, auth_exp=30 * 60 * 60)
    return Res(api, headers=headers)
