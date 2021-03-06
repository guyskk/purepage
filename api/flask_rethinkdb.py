import rethinkdb as r
from flask import _app_ctx_stack as stack


class Rethinkdb:

    def __init__(self, app, setups=None):
        """
        A flask wrapper of rethinkdb

        :param app: Flask
        :param setups: ReQLs for setup database
        """
        self.app = app
        if setups:
            self.setups = setups
        else:
            self.setups = []
        app.config.setdefault('RETHINKDB_HOST', 'localhost')
        app.config.setdefault('RETHINKDB_PORT', '28015')
        app.config.setdefault('RETHINKDB_AUTH', '')
        app.config.setdefault('RETHINKDB_DB', 'test')

        @app.teardown_appcontext
        def teardown_appcontext(exception):
            ctx = stack.top
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
            for op in self.setups:
                try:
                    op.run(conn)
                except r.errors.ReqlOpFailedError:
                    pass

    def drop_all(self):
        """Drop database"""
        db = self.app.config["RETHINKDB_DB"]
        with self.connect() as conn:
            r.db_drop(db).run(conn)

    @property
    def conn(self):
        ctx = stack.top
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
