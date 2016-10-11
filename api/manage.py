"""Purepage Commands"""
import click
from flask.cli import FlaskGroup
from purepage import create_app
from purepage.ext import db, r
from purepage.util import create_root

import config_develop as config
app = create_app(config)

cli = FlaskGroup(create_app=lambda *args, **kwargs: app, help=__doc__)


@cli.command("db", short_help="Config database")
@click.option("--create", "-c", is_flag=True,
              help="Create database and tables")
@click.option("--drop", "-d", is_flag=True,
              help="Drop database")
@click.option("--root", "-r", is_flag=True,
              help="Create root user")
def db_command(create, drop, root):
    if create:
        db.create_all()
        click.echo("create, OK")
    if drop:
        db.drop_all()
        click.echo("drop, OK")
    if root:
        create_root()
        click.echo("root, OK")


if __name__ == '__main__':
    cli()
