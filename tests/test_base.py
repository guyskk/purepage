# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function


def test_base(app):
    with app.test_client() as c:
        resp = c.get("/api/article/list")
        assert resp.status_code == 200
        resp = c.post("/api/user/signup")
        assert resp.status_code == 400
