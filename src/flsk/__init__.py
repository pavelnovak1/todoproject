import os
from database.db import init_app
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="secret",
        DATABASE=os.path.join(app.instance_path, "db.sqlite"))
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)
    from . import auth, application
    app.register_blueprint(auth.bp)
    app.register_blueprint(application.bp)

    return app
