"""Main application initialization and configuration.

Contains the code that creates and configures the Flask application.
"""

import os

from flask import Flask

from init import db, ma, bcrypt, jwt, mail
from controllers import cli, auth, user


def create_app():
    """Create and configure an instance of the Flask application.

    This function creates and configures an instance of the Flask
    application. It is used to create the application in the main
    entry point of the application.

    Returns
    -------
    Flask
        The configured Flask application.
    """
    # Create the Flask application
    app = Flask(__name__)

    # Disable sorting of JSON keys
    app.json.sort_keys = False

    # Load the database URI from the environment
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    # Load the JWT secret key from the environment
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # Load the security password salt from the environment
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get(
        'SECURITY_PASSWORD_SALT')

    # Initialize the Flask-SQLAlchemy extension
    db.init_app(app)

    # Initialize the Flask-Marshmallow extension
    ma.init_app(app)

    # Initialize the Flask-Bcrypt extension
    bcrypt.init_app(app)

    # Initialize the Flask-JWT-Extended extension
    jwt.init_app(app)

    # Initialize the Flask-Mail extension
    mail.init_app(app)

    # Register the CLI blueprint
    app.register_blueprint(cli)

    # Register the user blueprint
    app.register_blueprint(user)

    # Register the auth blueprint
    app.register_blueprint(auth)

    # Return the configured Flask application
    return app


app = create_app()
