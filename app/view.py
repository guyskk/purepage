# coding:utf-8

from __future__ import unicode_literals
from flask import request, render_template
from . import app
from . import article


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/article/<name>')
def page_article(name):
    data = article.get_article(name)
    return render_template("article.html", **data)
