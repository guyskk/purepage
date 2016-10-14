import flask
from flask_restaction import Res
from requests import HTTPError
from purepage import create_app
from purepage.ext import db
from purepage.util import create_root
import config_develop as config
import pytest
from contextlib import contextmanager
import json


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
def root(app):
    with app.app_context():
        create_root()
    res = Res(test_client=app.test_client)
    res.user.post_login({"account": "root", "password": "123456"})
    return res


@pytest.fixture
def user(app):
    def _user(id, password="123456", **kwargs):
        res = Res(test_client=app.test_client)
        res.user.post_signup({
            "id": id,
            "password": password,
            **kwargs
        })
        res.user.post_login({
            "account": id,
            "password": password,
        })
        return res
    return _user


@pytest.fixture(scope="session")
def assert_error():
    @contextmanager
    def _assert_error(status, error=None):
        with pytest.raises(HTTPError) as exinfo:
            yield
        resp = exinfo.value.response
        assert resp.status_code == status
        if error:
            if isinstance(resp, flask.Response):
                data = json.loads(resp.data.decode("utf-8"))
            else:
                data = resp.json()
            assert data["error"] == error
    return _assert_error
