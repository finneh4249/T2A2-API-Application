"""
This module contains the authentication endpoints for the API.

The endpoints are:

- **POST /login**: Authenticates a user and returns a JWT token.
- **POST /register**: Creates a new user.
- **POST /forgot_password**: Sends a forgot password email to the user.
- **POST /reset_password**: Resets a user's password if the token is valid.
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, decode_token
from datetime import datetime

from init import db, bcrypt
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
    # Get the username and password from the request body
    username = request.json.get('username')
    password = request.json.get('password')

    # Check if the username or password are missing
    if not username or not password:
        # Return an error if either are missing
        return 'Missing username or password', 400

    # Check if the user is already logged in
    if get_jwt_identity():
        # Return an error if the user is already logged in
        return {"message": "User is already logged in"}, 400

    # Get the user from the database
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        # Return an error if the user does not exist or the password is incorrect
        return 'Wrong username or password', 401

    # Create a JWT token for the user
    token = create_access_token(identity=user.id)

    # Return the logged-in user and the JWT token
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
    - OPTIONAL: `bio`: The new user's bio.

    Returns a JSON representation of the newly created user.

    If the user is already logged in, an error response is returned.
    """
    # Check that the user is not already logged in
    if get_jwt_identity():
        # Return an error if the user is already logged in
        return {"message": "User is already logged in"}, 400

    # Get the username, email, and password from the request body
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    bio = request.json['bio'] or None  # Get the bio, but don't require it

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

    return {
        "message": "User created successfully",
        "user": new_user,
        "confirmation_url": confirmation_url
    }

#TODO: Add delete user endpoint

@auth_controller.route('/confirm/<token>', methods=['POST'])
def confirm(token):
    """
    Confirms a user's account.

    The `token` is the confirmation token sent to the user's email address.

    Returns a JSON message indicating the status of the confirmation.
    """
    # Decode the token to get the user's ID
    # The `sub` key contains the user's ID
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
    # Set the `is_confirmed` attribute to `True`
    # Set the `confirmed_on` attribute to the current datetime
    user.is_confirmed = True
    user.confirmed_on = datetime.now()
    db.session.commit()

    # Return the confirmed user
    # Dump the `user` object to a JSON representation
    # Use the `profile_schema` to dump the user object
    return {"message": "User confirmed successfully, you may now log in.", "user": profile_schema.dump(user)}

@auth_controller.route('/forgot-password', methods=['GET'], endpoint="forgot_user_password")
def forgot_password():
    """
    Sends a password reset email to the user.

    The request body must contain the following JSON key:

    - `email`: The email address of the user.

    Returns a JSON message indicating the status of the password reset email.
    """
    # Get the user ID from the JWT
    user_id = request.args.get('user_id', type=int)

    # Get the user from the database
    user = User.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404

    # Create a password reset token
    # The `create_access_token` function creates a JWT token that contains the user's ID
    # The `identity` parameter is the user's ID
    # The `expires_delta` parameter is the amount of time the token is valid for
    # The `fresh` parameter is a boolean that indicates if the token is fresh or not
    # The `type` parameter is the type of token to create, either `access` or `refresh`
    token = create_access_token(
        identity=user_id,
        expires_delta=timedelta(hours=24),
        fresh=True,
        type='access'
    )

    # Send the password reset email
    # The `reset_url` is the URL that the user will visit to reset their password
    # The URL is constructed from the base URL of the application and the token
    reset_url = f"{request.url_root}auth/reset-password/{token}"

    return {
        "message": "Password reset link created. Normally this would be sent to your email. For the purpose of this assignment, the link will be displayed here.",
        "reset_url": reset_url
    }

@auth_controller.route('/reset-password/<token>', methods=['PUT', 'PATCH'], endpoint='reset_user_password_confirm')
def reset_password(token):
    """
    Resets a user's password.

    The request body must contain the following
    JSON keys:

    - `password`: The new password for the user.

    Returns a JSON message indicating the status of the password reset.
    """
    # Decode the token
    # The `decode_token` function decodes the JWT token
    # The `sub` parameter is the user's ID
    # The `token` parameter is the JWT token
    decoded_token = decode_token(token)
    user_id = decoded_token['sub']

    # Get the new password from the request body
    # The `request.json` is the JSON data in the request body
    # The `password` parameter is the new password for the user
    password = request.json['password']

    # Hash the password
    # The `bcrypt.generate_password_hash` function hashes the password
    # The `password` parameter is the password to hash
    # The `decode` function decodes the bytes to a UTF-8 string
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Update the user's password in the database
    # The `User.query.get` function retrieves the user from the database
    # The `user_id` parameter is the user's ID
    # The `password_hash` attribute is the hashed password
    # The `db.session.commit` function saves the changes to the database
    user = User.query.get(user_id)
    user.password_hash = hash_password
    db.session.commit()

    # Return the updated user
    # The `profile_schema.dump` function serializes the user
    # The `user` parameter is the user to serialize
    # The `message` parameter is the message to return
    return {"message": "Password reset successfully", "user": profile_schema.dump(user)}

@auth_controller.route('/change-password', methods=['PUT', 'PATCH'], endpoint="change_user_password")
@jwt_required()
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

    # Check that the new password is different from the old password
    if old_password == new_password:
        return {"message": "Password cannot be the same as previous password"}, 400

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
    return {
        "message": "Password changed successfully",
        "user": profile_schema.dump(user)
    }
