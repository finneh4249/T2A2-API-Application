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


@user_controller.route('/register', methods=['POST'])
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

    hash_password = bcrypt.generate_password_hash(password.encode('utf-8'))


    user = User(username=username, email=email, password_hash=hash_password)
    db.session.add(user)
    db.session.commit()
    #TODO: Add a confirmation email to send to the users email

    return user_schema.jsonify(user)


@user_controller.route('/login', methods=['POST'])
def login():
    """
    Logs in a user by checking their username and password.

    Request body must contain the following JSON keys:

    - `username`: The user's username.
    - `password`: The user's password.

    Returns a JSON representation of the logged-in user.
    """
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(password.encode('utf-8'), user.password_hash):
        create_access_token = jwt.create_access_token(identity=user.id)
        return profile_schema.jsonify(user), create_access_token
    return 'Wrong username or password', 401

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
    return user_schema.jsonify(user)