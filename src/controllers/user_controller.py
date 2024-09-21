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
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

from init import db, bcrypt
from models.user import User, user_schema, users_schema, profile_schema, UserSchema

user_controller = Blueprint('user_controller', __name__, url_prefix='/users')

@user_controller.route('/', methods=['GET'])
#TODO: Add Authentication?
def get_users():
    """
    Gets a list of all users in the database.

    Returns
    -------
    list of User
        A list of all users in the database.
    """
    users = User.query.all()
    user_arr = users_schema.jsonify(users)
    return user_arr


@user_controller.route('/profile/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Gets a specific user in the database.

    Parameters
    ----------
    user_id : int
        The ID of the user to get.

    Returns
    -------
    User
        The user with the specified ID.
    """
    user = User.query.get(user_id)
    return profile_schema.jsonify(user)
