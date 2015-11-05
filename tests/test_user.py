# coding:utf-8
from __future__ import unicode_literals
from kkblog import create_app, db
from pony.orm import db_session
import json
import pytest


@pytest.fixture()
def app():
    db.drop_all_tables(with_all_data=True)
    app = create_app()
    return app



def test_create_app():
    for i in range(10):
        db.drop_all_tables(with_all_data=True)
        with db_session:
            assert True
        app = create_app()


def login(app, username, password):
    with app.test_client() as c:
        data = {
            "username": username,
            "password": password
        }
        resp = c.post("/api/user/login", data=data)
        assert resp.status_code == 200
        token = resp.headers["Authorization"]
        return token


def register(app, email, password):
    with app.test_client() as c:
        data = {
            "email": email,
            "password": password
        }
        resp = c.post("/api/user/register", data=data)
        assert resp.status_code == 200
        return resp.data


def getme(app, token):
    with app.test_client() as c:
        headers = {"Authorization": token}
        resp = c.get("/api/user/me", headers=headers)
        assert resp.status_code == 200
        return resp.data


def test_login(app):
    # 登录
    token = login(app, "admin@admin.com", "123456")
    # 获取个人信息
    data = getme(app, token)
    u = json.loads(data)
    assert u["username"] == "admin@admin.com"


def test_register(app):
    uname = "1316792450@qq.com"
    # 注册
    data = register(app, uname, "123456")
    u = json.loads(data)
    # 注册成功
    assert u["username"] == uname
    # 登录
    token = login(app, uname, "123456")
    # 获取个人信息
    data = getme(app, token)
    u = json.loads(data)
    assert u["username"] == uname
