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

    The request body must contain the following JSON keys:

    - `username`: The user's username.
    - `password`: The user's password.

    Returns a JSON representation of the logged-in user, including
    a JWT token in the `token` field.

    If the user is already logged in, or if the username or password
    are incorrect, an error response is returned.
    """
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return 'Missing username or password', 400

    if get_jwt_identity():
        return {"message": "User is already logged in"}, 400

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return 'Wrong username or password', 401

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

    # Hash the password
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create the user in the database
    user = User(username=username, email=email,
                password_hash=hash_password, is_confirmed=False)
    db.session.add(user)
    db.session.commit()

    # Send confirmation email to the user
    token = create_access_token(identity=user.id)
    confirmation_url = f"{request.url_root}auth/confirm/{token}"

    # Return a JSON representation of the newly created user
    new_user = user_schema.dump(user)

    return {"message": "User created successfully", "user": new_user, "confirmation_url": confirmation_url}


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


@auth_controller.route('/forgot_password', methods=['GET'])
@jwt_required
def forgot_password():
    """
    Sends a password reset email to the user.

    The request body must contain the following JSON key:

    - `email`: The email address of the user.

    Returns a JSON message indicating the status of the password reset email.
    """
    # Get the user ID from the JWT
    user_id = get_jwt_identity()

    # Get the user from the database
    user = User.query.get(user_id)

    # Create a password reset token
    token = create_access_token(identity=user_id)

    # Send the password reset email
    reset_url = f"{request.url_root}auth/reset_password/{token}"

    return {"message": "Password reset link created", "reset_url": reset_url}


@auth_controller.route('/reset_password/<token>', methods=['PUT', 'PATCH'], endpoint='reset_user_password')
def reset_password(token):
    """
    Resets a user's password.

    The request body must contain the following
    JSON keys:

    - `password`: The new password for the user.

    Returns a JSON message indicating the status of the password reset.
    """
    # Get the user ID from the JWT
    user_id = get_jwt_identity()

    # Decode the token
    decoded_token = decode_token(token)
    user_id = decoded_token['sub']

    if user_id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401

    # Get the new password from the request body
    password = request.json['password']

    # Hash the password
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Update the user's password in the database
    user = User.query.get(user_id)
    user.password_hash = hash_password
    db.session.commit()

    # Return the updated user
    return {"message": "Password reset successfully", "user": profile_schema.dump(user)}

@auth_controller.route('/change_password', methods=['PUT', 'PATCH'], endpoint="change_user_password")
@jwt_required
def change_password():
    """
    Changes a user's password.

    The request body must contain the following
    JSON keys:

    - `old_password`: The user's current password.
    - `new_password`: The user's new password.

    Returns a JSON message indicating the status of the password change.
    """
    # Get the user ID from the JWT
    user_id = get_jwt_identity()

    # Get the old and new passwords from the request body
    old_password = request.json['old_password']
    new_password = request.json['new_password']

    # Get the user from the database
    user = User.query.get(user_id)

    # Check that the old password is correct
    if not bcrypt.check_password_hash(user.password_hash, old_password):
        return {"message": "Incorrect password"}, 401

    # Hash the new password
    hash_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    # Update the user's password in the database
    user.password_hash = hash_password
    db.session.commit()

    # Return the updated user
    return {"message": "Password changed successfully", "user": profile_schema.dump(user)}