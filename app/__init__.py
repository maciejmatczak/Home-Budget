import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'db.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app.models import db, init_db_command, mock_db_command
    db.init_app(app)
    app.cli.add_command(init_db_command)
    app.cli.add_command(mock_db_command)

    from app.budgeter import load_dumps_command
    app.cli.add_command(load_dumps_command)

    # from . import dashboard
    # app.register_blueprint(dashboard.bp)

    # app.add_url_rule('/', endpoint='index')

    from . import api
    app.register_blueprint(api.bp, url_prefix='/api')

    return app
