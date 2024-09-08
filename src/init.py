"""
The `init` module is used to configure the Flask extensions for the
application.

The extensions used in the application are:

- `flask_sqlalchemy.SQLAlchemy` for interacting with the database.
- `flask_marshmallow.Marshmallow` for serializing and deserializing data.
- `flask_bcrypt.Bcrypt` for hashing passwords.
- `flask_jwt_extended.JWTManager` for managing JWT tokens.

"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

