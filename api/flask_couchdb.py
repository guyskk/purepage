import couchdb


class CouchDB(couchdb.CouchDB):
    """Flask-CouchDB"""

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        url = app.config["COUCHDB_DATABASE"]
        try:
            self.init(url)
        except Exception as ex:
            app.logger.warn("Can't connect couchdb[%s], will connect again"
                            " before first request:\n%s" % (url, ex))
            self.init(url, skip_setup=True)
            app.before_first_request(lambda: self.init(url))
