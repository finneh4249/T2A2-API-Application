from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.follow import Follow, follow_schema, follows_schema
from models.user import User, user_schema, users_schema


follow_controller = Blueprint('follow_controller', __name__, url_prefix='/users/<int:user_id>')

@follow_controller.route('/following', methods=['GET'], endpoint='get_following')
@jwt_required()
def get_follows(user_id):
    """
    Get all follows for a user.

    Parameters
    ----------
    user_id : int
        ID of the user to get follows for.

    Returns
    -------
    str
        JSON representation of the follows.
    """
    follows = Follow.query.filter_by(follower_id=user_id).all()
    return follows_schema.jsonify(follows)

@follow_controller.route('/followers', methods=['GET'], endpoint='get_followers')
@jwt_required()
def get_followers(user_id):
    """
    Get all followers for a user.

    Parameters
    ----------
    user_id : int
        ID of the user to get followers for.

    Returns
    -------
    str
        JSON representation of the followers.
    """
    followers = Follow.query.filter_by(followed_id=user_id).all()
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
    user = User.query.get(user_id)
    if not user:
        return 'User not found', 404

    current_user_id = get_jwt_identity()
    if current_user_id == user_id:
        return 'Cannot follow yourself', 400
    new_follow = Follow(follower_id=current_user_id, followed_id=user_id)
    db.session.add(new_follow)
    db.session.commit()
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
    current_user_id = get_jwt_identity()
    new_follow = Follow.query.filter_by(follower_id=current_user_id, followed_id=user_id).first()
    if not new_follow:
        return 'Follow not found', 404
    db.session.delete(new_follow)
    db.session.commit()
    return follow_schema.jsonify(new_follow)

#TODO: Add friends functionality, if a user follows another user and that user follows the first user, they are friends
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
    user = User.query.get(user_id)
    if not user:
        return 'User not found', 404

    friends = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()
    friends_arr = users_schema.dump(friends)
    return friends_arr

# Define an algorithm to suggest friends for a user, based on the friends of their friends
@follow_controller.route('/suggested_friends', methods=['GET'])
@jwt_required()
def get_suggested_friends(user_id):
    """
    Get suggested friends for a user.

    Parameters
    ----------
    user_id : int
        ID of the user to get suggested friends for.

    Returns
    -------
    list of User
        The user's suggested friends.
    """
    user = User.query.get(user_id)
    if not user:
        return 'User not found', 404

    # Get all friends of the user
    friends = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()
    friends_ids = [friend.id for friend in friends]

    # Get all users who are followed by the user's friends but not the user and filter out the user's friends
    suggested_friends = User.query.join(Follow, Follow.follower_id.in_(friends_ids)).filter(Follow.followed_id != user_id).filter(Follow.followed_id.notin_(friends_ids)).all()

    suggested_friends_arr = users_schema.dump(suggested_friends)
    return suggested_friends_arr