import sqlite3 as sql

import click
from flask import current_app, g
from flask.cli import with_appcontext


def db_init():
    """Initialize new database"""
    database = db_connect()
    with open('database\\db_init.sql') as init_sql:
        database.executescript(init_sql.read())


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db_init()
    click.echo('Initialized the database.')


def db_connect():
    """Establish connection to database"""
    if 'db' not in g:
        g.db = sql.connect(current_app.config["DATABASE"], detect_types=sql.PARSE_DECLTYPES)
        g.db.row_factory = sql.Row
    return g.db


def db_close(e=None):
    """Close connection to database"""
    database = g.pop('db', None)

    if database:
        database.close()


def init_app(app):
    app.teardown_appcontext(db_close)
    app.cli.add_command(init_db_command)
