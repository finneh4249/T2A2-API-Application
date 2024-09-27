"""
This module contains the API endpoints for follow-related operations.

The endpoints are:

- **GET /users/<user_id>/follows**: Get all users that the user is following.
- **POST /users/<user_id>/follow**: Follow a user.
- **DELETE /users/<user_id>/follow**: Unfollow a user.
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.follow import Follow, follow_schema, follows_schema
from models.user import User, users_schema


follow_controller = Blueprint(
    'follow_controller', __name__, url_prefix='/users/<int:user_id>')


@follow_controller.route('/following', methods=['GET'], endpoint='get_following')
@jwt_required()
def get_follows(user_id):
    """
    Gets all users that the user is following.

    Parameters
    ----------
    user_id : int
        The ID of the user to get follows for.

    Returns
    -------
    str
        JSON representation of the follows.

    Notes
    -----
    The returned JSON will be a list of users, each with their
    id, username, email, and profile_picture.
    """
    follows = Follow.query.filter_by(follower_id=user_id).all()
    return follows_schema.jsonify(follows)


@follow_controller.route('/followers', methods=['GET'], endpoint='get_followers')
@jwt_required()
def get_followers(user_id):
    """
    Gets all followers for a user.

    Parameters
    ----------
    user_id : int
        The ID of the user to get followers for.

    Returns
    -------
    str
        JSON representation of the followers.

    Notes
    -----
    The returned JSON will be a list of users, each with their
    id, username, email, and profile_picture.
    """
    followers = Follow.query.filter_by(followed_id=user_id).all()
    # Return the followers as a list of user objects
    return follows_schema.jsonify(followers)


@follow_controller.route('/follow', methods=['POST'])
@jwt_required()
def create_follow(user_id):
    """
    Follow a user.

    Parameters
    ----------
    user_id : int
        ID of the user to follow.

    Returns
    -------
    str
        JSON representation of the follow.
    """
    # Get the user to follow
    user = User.query.get(user_id)
    if not user:
        return 'User not found', 404

    # Get the current user's ID
    current_user_id = get_jwt_identity()

    # Check if the current user is trying to follow themselves
    if current_user_id == user_id:
        return 'Cannot follow yourself', 400

    # Create a new follow
    new_follow = Follow(follower_id=current_user_id, followed_id=user_id)

    # Add the follow to the database and commit the changes
    db.session.add(new_follow)
    db.session.commit()

    # Return the follow as JSON
    return follow_schema.jsonify(new_follow)


@follow_controller.route('/follow', methods=['DELETE'], endpoint='unfollow')
@jwt_required
def unfollow(user_id):
    """
    Unfollow a user.

    Parameters
    ----------
    user_id : int
        ID of the user to unfollow.

    Returns
    -------
    str
        JSON representation of the follow.
    """
    # Get the current user's ID
    current_user_id = get_jwt_identity()

    # Get the follow to delete
    new_follow = Follow.query.filter_by(
        follower_id=current_user_id, followed_id=user_id).first()

    # Check if the follow was found
    if not new_follow:
        return 'Follow not found', 404

    # Delete the follow
    db.session.delete(new_follow)
    db.session.commit()

    # Return the deleted follow as JSON
    return follow_schema.jsonify(new_follow)


@follow_controller.route('/friends', methods=['GET'])
@jwt_required()
def get_user_friends(user_id):
    """
    Get all friends for a user.

    Parameters
    ----------
    user_id : int
        ID of the user to get friends for.

    Returns
    -------
    list of User
        The user's friends.
    """
    # Get the user
    user = User.query.get(user_id)
    if not user:
        return 'User not found', 404

    # Get the user's friends
    friends = User.query.join(Follow, Follow.followed_id == User.id) \
        .filter(Follow.follower_id == user_id) \
        .all()

    # Serialize the friends
    friends_arr = users_schema.dump(friends)

    # Return the serialized friends
    return friends_arr


@follow_controller.route('/suggested_friends', methods=['GET'])
@jwt_required()
def get_suggested_friends(user_id):
    """
    Get suggested friends for a user.

    This endpoint returns a list of users that are friends with the user's friends but not friends with the user themselves.

    Parameters
    ----------
    user_id : int
        ID of the user to get suggested friends for.

    Returns
    -------
    list of User
        The user's suggested friends.
    """
    # Get the user
    user = User.query.get(user_id)
    if not user:
        return 'User not found', 404

    # Get all friends of the user
    friends = User.query.join(Follow, Follow.followed_id == User.id) \
        .filter(Follow.follower_id == user_id) \
        .all()

    # Get all users who are followed by the user's friends but not the user and filter out the user's friends
    friends_ids = [friend.id for friend in friends]
    suggested_friends = User.query.join(Follow, Follow.follower_id.in_(friends_ids)) \
        .filter(Follow.followed_id != user_id) \
        .filter(Follow.followed_id.notin_(friends_ids)) \
        .all()

    # Serialize the suggested friends
    suggested_friends_arr = users_schema.dump(suggested_friends)

    # Return the serialized suggested friends
    return suggested_friends_arr
