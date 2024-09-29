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

from models.user import User, user_schema, users_schema, profile_schema
from models.post import Post, posts_schema
from .follow_controller import follow_controller
user_controller = Blueprint('user_controller', __name__, url_prefix='/users')

user_controller.register_blueprint(follow_controller)


@user_controller.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """
    Gets a list of all users in the database.

    Returns
    -------
    list of User
        A list of all users in the database.
    """
    # Get the page number from the request query parameters, default to 1
    page = request.args.get('page', 1, type=int)

    # Get the number of posts to retrieve per page from the request query
    # parameters, default to 10
    per_page = request.args.get('per_page', 10, type=int)

    users = User.query.all()
    paginated_users = users.paginate(
        page=page, per_page=per_page, error_out=False)
    user_arr = users_schema.jsonify(paginated_users.items)
    return user_arr


@user_controller.route('/<user_id>/profile', methods=['GET'])
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
    if not user:
        return 'User not found', 404

    return profile_schema.jsonify(user)


@user_controller.route('/<user_id>/profile', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    """
    Updates a user in the database.

    The 

    Parameters
    ----------
    user_id : int
        The ID of the user to update.

    Returns
    -------
    User
        The updated user.
    """
    user = User.query.get(user_id)
    if not user:
        return 'User not found', 404

    if user.id != get_jwt_identity() and not user.is_admin:
        return 'Unauthorized', 401

    data = request.json

    user.username = data['username'] or user.username
    user.email = data['email'] or user.email
    user.bio = data['bio'] or user.bio

    db.session.commit()

    profile = profile_schema.dump(user)
    message = f"User {user.username} updated successfully."
    return {"message": message, "user": profile}


@user_controller.route('/<user_id>/timeline', methods=['GET'])
@jwt_required()
def get_user_timeline(user_id):
    """
    Gets a user's timeline.

    Parameters
    ----------
    user_id : int
        The ID of the user whose timeline to get.

    Returns
    -------
    list of Post
        The user's timeline.
    """
    user = User.query.get(user_id)
    if not user:
        return 'User not found', 404

    posts = Post.query.filter_by(author_id=user_id).order_by(
        Post.created_at.desc()).all()
    post_arr = posts_schema.dump(posts)
    return post_arr
