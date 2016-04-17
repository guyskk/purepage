# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from couchdb_client import Server, Database, CouchdbException


class CouchDB(object):
    """CouchDB"""

    def __init__(self, app=None):
        self.server = None
        self.db = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.server = Server(app.config["COUCHDB_SERVER"])
        db_url = app.config["COUCHDB_SERVER"] + \
            '/' + app.config["COUCHDB_DATABASE"]
        self.db = Database(db_url)
        try:
            self.db.head()
        except CouchdbException as ex:
            if ex.status_code == 404:
                self.db.put()
            else:
                raise
