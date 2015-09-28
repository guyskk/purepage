# coding:utf-8

from __future__ import unicode_literals
from pony.orm import Database
from flask import Flask
app = Flask(__name__)
app.config.from_object('app.default_config')

db = Database()

from flask import Blueprint, render_template
from flask_restaction import Api
from pony.orm import sql_debug
from .article import Article
from .githooks import GitHooks
from . import view
bp_api = Blueprint('api', __name__, static_folder='static')

api = Api(bp_api)
api.add_resource(Article)
api.add_resource(GitHooks)

app.register_blueprint(bp_api, url_prefix='/api')


@app.before_first_request
def init():
    print "--init--" * 10
    api.gen_resjs()
    api.gen_resdocs()
    sql_debug(True)

    db.bind(app.config["DATABASE_NAME"],
            app.config["DATABASE_PATH"],
            create_db=True)
    db.generate_mapping(create_tables=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
