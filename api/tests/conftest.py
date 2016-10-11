from flask_restaction import Res
from purepage import create_app
from purepage.ext import db
from purepage.util import create_root
import config_develop as config
import pytest


@pytest.fixture
def app():
    app = create_app(config)
    db.create_all()
    yield app
    db.drop_all()


@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c


@pytest.fixture
def res(app):
    return Res(test_client=app.test_client)


@pytest.fixture
def root(app, res):
    with app.app_context():
        create_root()
    res.user.post_login({"username": "root", "password": "123456"})
    return res


@pytest.fixture
def user(res):
    def _user(username, password="123456", **kwargs):
        res.user.post_signup({
            "username": username,
            "password": password,
            **kwargs
        })
        res.user.post_login({
            "username": username,
            "password": password,
        })
        return res
    return _user
