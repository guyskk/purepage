import rethinkdb as r
from flask import _app_ctx_stack  # use this if no request context
from flask import _request_ctx_stack  # a connection per request


class Rethinkdb:

    def __init__(self, app, tables=None):
        self.app = app
        if tables:
            self.tables = tables
        else:
            self.tables = []
        app.config.setdefault('RETHINKDB_HOST', 'localhost')
        app.config.setdefault('RETHINKDB_PORT', '28015')
        app.config.setdefault('RETHINKDB_AUTH', '')
        app.config.setdefault('RETHINKDB_DB', 'test')

        @app.teardown_request
        def teardown_request(exception):
            ctx = _request_ctx_stack.top
            if hasattr(ctx, 'rethinkdb'):
                ctx.rethinkdb.close()

        @app.teardown_appcontext
        def teardown_appcontext(exception):
            ctx = _app_ctx_stack.top
            if hasattr(ctx, 'rethinkdb'):
                ctx.rethinkdb.close()

    def connect(self):
        """Create a connect"""
        host = self.app.config['RETHINKDB_HOST']
        port = self.app.config['RETHINKDB_PORT']
        auth = self.app.config['RETHINKDB_AUTH']
        db = self.app.config['RETHINKDB_DB']
        return r.connect(host=host, port=port, auth_key=auth, db=db)

    def create_all(self):
        """Create database and tables"""
        db = self.app.config["RETHINKDB_DB"]
        with self.connect() as conn:
            try:
                r.db_create(db).run(conn)
            except r.errors.RqlRuntimeError:
                pass
            for table in self.tables:
                try:
                    r.table_create(table).run(conn)
                except r.errors.ReqlOpFailedError:
                    pass

    def drop_all(self):
        """Drop database"""
        db = self.app.config["RETHINKDB_DB"]
        with self.connect() as conn:
            r.db_drop(db).run(conn)

    @property
    def conn(self):
        ctx = _request_ctx_stack.top
        if ctx is None:
            ctx = _app_ctx_stack.top
        if ctx is None:
            raise RuntimeError("Working outside of context")
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

    def pagging(self, q, page, per_page):
        return self.run(
            q.skip((page - 1) * per_page)
            .limit(per_page)
        )
