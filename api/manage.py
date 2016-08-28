"""Purepage Commands"""
import click
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError
from flask.cli import FlaskGroup, run_command as flask_run_command
from purepage import create_app, create_connect

app = create_app()
cli = FlaskGroup(create_app=lambda *args, **kwargs: app, help=__doc__)


@cli.command('run', short_help='Runs a development server.')
@click.option('--host', '-h', default='127.0.0.1', help='Host to bind')
@click.option('--port', '-p', default=5000, help='Port to bind')
@click.option('--debug/--no-debug', '-d', default=None, help='Debug or not')
def run_command(host, port, debug):
    if debug is None:
        debug = app.debug
    flask_run_command.callback(
        host=host, port=port, reload=debug, debugger=debug,
        eager_loading=None, with_threads=False
    )


@cli.command('db', short_help='Config database')
@click.option('--setup', is_flag=True, help='Setup database or not')
def db_command(setup):
    if setup:
        db = app.config['RETHINKDB_DB']
        conn = create_connect(app)
        try:
            r.db_create(db).run(conn)
            click.echo('Database setup completed.')
        except RqlRuntimeError:
            click.echo('App database already exists.')
    else:
        click.echo('Nothing to do.')

if __name__ == '__main__':
    try:
        import ipdb as pdb
    except:
        import pdb
    __builtins__.debug = pdb.set_trace
    cli()
