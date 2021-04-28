import os

from flask import Flask

import database.db as db

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="secret",
    DATABASE=os.path.join(app.instance_path, "db.sqlite"))
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.db_init(app)
db.db_close(app)