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
def root(app):
    with app.app_context():
        create_root()
    res = Res(test_client=app.test_client)
    res.user.post_login({"username": "root", "password": "123456"})
    return res


def test_root(root):
    me = root.user.get_me()
    assert me["username"] == "root"
    assert me["role"] == "root"
