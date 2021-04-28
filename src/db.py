import sqlite3 as sql
from flask import g as globals


def db_init():
    """Initialize new database"""
    database = db_connect()
    with open('db_init.sql') as init_sql:
        database.executescript(init_sql.read())


def db_connect():
    """Establish connection to database"""
    if 'database' not in globals:
        globals.database = sql.connect('db.sglite', detect_types=sql.PARSE_DECLTYPES)
        globals.database.row_factory = sql.Row
    return globals.database


def db_close():
    """Close connection to database"""
    database = globals.pop('database', None)

    if database:
        database.close()

