"""
This module contains the API endpoints for user-related operations.

The endpoints are:

- **GET /users**: Get a list of all users.
- **GET /users/<user_id>**: Get a specific user.
- **POST /users**: Create a new user.
- **PUT /users/<user_id>**: Update a user.
- **DELETE /users/<user_id>**: Delete a user.

"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user import User, user_schema, users_schema

user_controller = Blueprint('user_controller', __name__, url_prefix='/users')

@user_controller.route('/', methods=['GET'])
def get_users():
    """
    Gets a list of all users in the database.

    Returns
    -------
    list of User
        A list of all users in the database.
    """
    users = User.query.all()
    return users_schema.jsonify(users)

@user_controller.route('/', methods=['POST'])
def create_user():
    """
    Creates a new user in the database.

    Request body must contain the following JSON keys:

    - `username`: The new user's username.
    - `email`: The new user's email address.
    - `password`: The new user's password.

    Returns a JSON representation of the newly created user.
    """
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    user = User(username=username, email=email, password_hash=password)
    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user)
