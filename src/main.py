"""Main application initialization and configuration.

Contains the code that creates and configures the Flask application.
"""

import os

from flask import Flask

from init import db, ma, bcrypt, jwt
from controllers.cli_controller import cli_controller
from controllers.user_controller import user_controller


def create_app():
    """Create and configure an instance of the Flask application.

    Returns
    -------
    Flask
        The configured Flask application.
    """
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(cli_controller)
    app.register_blueprint(user_controller)


    return app
