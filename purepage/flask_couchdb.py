import couchdb


class CouchDB(object):
    """CouchDB"""

    def __init__(self, app=None):
        self.db = None
        if app:
            self.init_app(app)

    def _setup(self):
        """setup couchdb"""
        self.db = couchdb.CouchDB(self.url)

    def init_app(self, app):
        self.url = app.config["COUCHDB_DATABASE"]
        try:
            self.db = couchdb.CouchDB(self.url)
        except Exception as ex:
            self.db = couchdb.CouchDB(self.url, skip_setup=True)
            app.logger.warn("Can't connect couchdb[%s], will connect again"
                            " before first request:\n%s" % (self.url, ex))
            app.before_first_request(self._setup)
