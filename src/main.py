"""Main application initialization and configuration.

Contains the code that creates and configures the Flask application.
"""

import os

from flask import Flask
from marshmallow import ValidationError

from init import db, ma, bcrypt, jwt
from controllers import cli, auth, user, post, feed, comment, like, follow



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

    # Initialize the Flask-SQLAlchemy extension
    db.init_app(app)

    # Initialize the Flask-Marshmallow extension
    ma.init_app(app)

    # Initialize the Flask-Bcrypt extension
    bcrypt.init_app(app)

    # Initialize the Flask-JWT-Extended extension
    jwt.init_app(app)

    # Register the CLI blueprint
    app.register_blueprint(cli)

    # Register the user blueprint
    app.register_blueprint(user)

    # Register the auth blueprint
    app.register_blueprint(auth)

    # Register the post blueprint
    app.register_blueprint(post)

    app.register_blueprint(feed)

    app.register_blueprint(comment)

    app.register_blueprint(like)

    app.register_blueprint(follow)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle a validation error by returning a 400 error response.

        This function is an error handler for validation errors. It
        takes a ValidationError object as an argument and returns a
        400 error response with a JSON body containing the error
        messages.

        Parameters
        ----------
        error : ValidationError
            The ValidationError object.

        Returns
        -------
        tuple
            A 400 error response with a JSON body containing the error
            messages.
        """
        return {"validation_error": error.messages}, 400

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle a generic error by returning a 500 error response.

        This function is an error handler for generic uncaught errors. It
        takes an Exception object as an argument and returns a 500 error
        response with a JSON body containing the error message.

        Parameters
        ----------
        error : Exception
            The Exception object.

        Returns
        -------
        tuple
            A 500 error response with a JSON body containing the error
            message.
        """
        return {"error": str(error)}, 500
        
    # Return the configured Flask application
    return app


app = create_app()

