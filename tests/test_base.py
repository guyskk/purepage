# coding:utf-8

from __future__ import unicode_literals


def test_app():
    from kkblog import create_app
    app = create_app()
    app.run(host="0.0.0.0", debug=True)
