"""
Authentication controller.

This module contains the endpoints for authentication and authorization.
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, decode_token
from datetime import datetime

from init import db, bcrypt, mail
from models.user import User, user_schema, profile_schema, UserSchema


auth_controller = Blueprint('auth', __name__, url_prefix='/auth')


@auth_controller.route('/login', methods=['POST'])
@jwt_required(optional=True)
def login():
    """
    Logs in a user by checking their username and password.

    This endpoint is used to log in a user and retrieve a JWT token.
    The request body must contain the following JSON keys:

    - `username`: The user's username.
    - `password`: The user's password.

    Returns a JSON representation of the logged-in user, including
    a JWT token in the `token` field.

    If the user is already logged in, or if the username or password
    are incorrect, an error response is returned.
    """
    # Check that the request body contains the necessary fields
    if not request.json or not request.json.get('username') or not request.json.get('password'):
        return 'Missing username or password', 400

    # Check that the user is not already logged in
    if get_jwt_identity():
        return {"message": "User is already logged in"}, 400

    # Get the username and password from the request body
    username = request.json['username']
    password = request.json['password']

    # Check for potential XSS vulnerabilities in the username
    if '<' in username or '>' in username:
        # TODO: Implement XSS protection
        return 'Invalid username', 400

    # Find the user in the database
    user = User.query.filter_by(username=username).first()

    # Check that the user exists and that the password is correct
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return 'Wrong username or password', 401

    # Create a JWT token for the user
    token = create_access_token(identity=user.id)
    return {"message": f"User {username} logged in successfully", "token": token}

@auth_controller.route('/register', methods=['POST'])
@jwt_required(optional=True)
def create_user():
    """
    Creates a new user in the database.

    Request body must contain the following JSON keys:

    - `username`: The new user's username.
    - `email`: The new user's email address.
    - `password`: The new user's password.

    Returns a JSON representation of the newly created user.
    """
    # Check that the user is not already logged in
    if get_jwt_identity():
        return {"message": "User is already logged in"}, 400

    # Get the username, email, and password from the request body
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    # Check for potential XSS vulnerabilities in the username and email
    if '<' in username or '>' in username or '<' in email or '>' in email:
        # TODO: Implement XSS protection
        return 'Invalid username or email', 400

    # Hash the password
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create the user in the database
    user = User(username=username, email=email, password_hash=hash_password, is_confirmed=False)
    db.session.add(user)
    db.session.commit()

    # Send confirmation email to the user
    token = create_access_token(identity=user.id)
    confirmation_url = f"{request.url_root}auth/confirm/{token}"

    # Return a JSON representation of the newly created user
    new_user = user_schema.dump(user)

    return {"message": "User created successfully", "user": new_user,"confirmation_url": confirmation_url}
@auth_controller.route('/confirm/<token>', methods=['GET'])
def confirm(token):
    """
    Confirms a user's account.

    The `token` is the confirmation token sent to the user's email address.

    Returns a JSON message indicating the status of the confirmation.
    """
    # Decode the token to get the user's ID
    decoded_token = decode_token(token)
    user_id = decoded_token['sub']

    # Get the user from the database
    user = User.query.filter_by(id=user_id).first()

    # If the user doesn't exist, return 404 error
    if user is None:
        return {"message": "User not found"}, 404

    # If the user is already confirmed, return 400 error
    if user.is_confirmed:
        return {"message": "User is already confirmed"}, 400

    # Confirm the user
    user.is_confirmed = True
    user.confirmed_on = datetime.now()
    db.session.commit()

    # Return the confirmed user
    return {"message": "User confirmed successfully, you may now log in.", "user": profile_schema.dump(user)}

