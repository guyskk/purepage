import rethinkdb as r
from flask import _app_ctx_stack as stack


class Rethinkdb:

    def __init__(self, app):
        self.app = app

        @app.teardown_request
        def teardown_request(exception):
            ctx = stack.top
            if hasattr(ctx, 'rethinkdb'):
                ctx.rethinkdb.close()

    def connect(self):
        host = self.app.config.setdefault('RETHINKDB_HOST', 'localhost')
        port = self.app.config.setdefault('RETHINKDB_PORT', '28015')
        auth = self.app.config.setdefault('RETHINKDB_AUTH', '')
        db = self.app.config.setdefault('RETHINKDB_DB', 'test')
        return r.connect(host=host, port=port, auth_key=auth, db=db)

    @property
    def conn(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'rethinkdb'):
                ctx.rethinkdb = self.connect()
            return ctx.rethinkdb

    def run(self, q):
        return q.run(self.conn)

    def first(self, q):
        data = list(q.limit(1).run(self.conn))
        if data:
            return data[0]
        else:
            return None
