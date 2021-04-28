import sqlite3 as sql


def db_init(app):
    """Initialize new database"""
    database = db_connect(app)
    with open('database/db_init.sql') as init_sql:
        database.executescript(init_sql.read())


def db_connect(app):
    """Establish connection to database"""
    if 'database' not in app.config:
        app.database = sql.connect(app.config["DATABASE"], detect_types=sql.PARSE_DECLTYPES)
        app.database.row_factory = sql.Row
    return app.database


def db_close(app):
    """Close connection to database"""
    database = app.database

    if database:
        database.close()

