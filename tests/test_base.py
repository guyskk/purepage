# coding:utf-8

from __future__ import unicode_literals


def test_app():
    from kkblog import create_app
    app = create_app()
    with app.test_client() as c:
        assert 200 == c.get("/").status_code
        assert 200 == c.get("/login").status_code
        assert 200 == c.get("/register").status_code
