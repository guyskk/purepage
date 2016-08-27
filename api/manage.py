"""Purepage Commands"""
import click
from flask.cli import FlaskGroup, run_command as flask_run_command
from purepage import create_app


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


@cli.command()
def db():
    """Runs a database command"""
    click.echo('db')

if __name__ == '__main__':
    try:
        import ipdb as pdb
    except:
        import pdb
    __builtins__.debug = pdb.set_trace
    cli()
