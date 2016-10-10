"""Purepage Commands"""
import click
from flask.cli import FlaskGroup
from purepage import create_app
from purepage.ext import r, db

import config_develop as config
app = create_app(config)

cli = FlaskGroup(create_app=lambda *args, **kwargs: app, help=__doc__)

ALL_TABLE = ["user"]


@cli.command("db", short_help="Config database")
@click.option("--setup", "-s", is_flag=True, help="Setup database or not")
def db_command(setup):
    if setup:
        try:
            db.run(r.db_create(app.config["RETHINKDB_DB"]))
            click.echo("Database %s, OK" % db)
        except r.errors.RqlRuntimeError:
            click.echo("Database %s, already exists" % db)
        for table in ALL_TABLE:
            try:
                db.run(r.table_create(table))
                click.echo("Table %s, OK" % table)
            except r.errors.ReqlOpFailedError:
                click.echo("Table %s, already exists" % table)
    else:
        click.echo("Nothing to do")

if __name__ == '__main__':
    cli()
