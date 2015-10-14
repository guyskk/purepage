# coding:utf-8

from __future__ import unicode_literals


def test_app():
    from kkblog import create_app
    app = create_app()
    with app.test_client() as c:
        assert 200 == c.get("/").status_code
        assert 200 == c.get("/login").status_code
        assert 200 == c.get("/register").status_code
        assert 200 == c.get("/api/article/list").status_code
        data = {"username": "admin@admin.com", "password": "123456"}
        login_resp = c.post("/api/user/login", data=data)
        assert 200 == login_resp.status_code
        assert "Authorization" in login_resp.headers
        data = {"local": False, "rebuild": True}
        assert 200 == c.post("/api/githooks/update", data=data, headers=login_resp.headers).status_code
