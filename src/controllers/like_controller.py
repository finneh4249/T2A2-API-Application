"""
This module contains the API endpoints for like-related operations.

The endpoints are:

- **POST /posts/<post_id>/like**: Like a post.
- **DELETE /posts/<post_id>/like**: Unlike a post.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.post import Post, post_schema
from models.like import Like, likes_schema
from models.user import User, user_schema


like_controller = Blueprint('like_controller', __name__, url_prefix='/posts/<int:post_id>')

@like_controller.route('/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    """
    Likes a post.

    Parameters
    ----------
    post_id : int
        The ID of the post to like.

    Returns
    -------
    Post
        The post that was liked.
    """

    # Get the post with the specified ID
    post = Post.query.get(post_id)
    if not post:
        # If the post does not exist, return a 404 error
        return {"message": "Post not found"}, 404

    user_id = get_jwt_identity()

    if user_id == post.author_id:
        # If the user is trying to like their own post, return a 400 error
        return {"message": "Cannot like own post"}, 400

    if any(like.user_id == user_id for like in post.likes):
        # If the user has already liked the post, return a 400 error
        return {"message": "Post already liked"}, 400

    # Create a new Like object and add it to the post's likes
    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()

    # Return the post in JSON format
    message = post_schema.dump(post)

    return message

@like_controller.route('/like', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id):
    """
    Unlikes a post.

    Parameters
    ----------
    post_id : int
        The ID of the post to unlike.

    Returns
    -------
    Post
        The post that was unliked.
    """
    # Get the post with the specified ID
    post = Post.query.get(post_id)
    if not post:
        # If the post does not exist, return a 404 error
        return {"message": "Post not found"}, 404

    # Get the ID of the authenticated user
    user_id = get_jwt_identity()

    # Check if the user has already liked the post
    if not any(like.user_id == user_id for like in post.likes):
        # If the user has not liked the post, return a 400 error
        return {"message": "Post not liked"}, 400

    # Find the Like object associated with the user and post
    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()

    # Delete the Like object
    db.session.delete(like)
    db.session.commit()

    # Return the post in JSON format
    return post_schema.dump(post)

@like_controller.route('/likes', methods=['GET'])
@jwt_required()
def get_likes(post_id):
    """
    Gets a list of users who have liked a post.

    Parameters
    ----------
    post_id : int
        The ID of the post to get likes for.

    Returns
    -------
    list of User
        A list of users who have liked the post.
    """
    # Check if the post exists
    post = Post.query.get(post_id)
    if not post:
        # If the post does not exist, return a 404 error
        return {"message": "Post not found"}, 404

    # Get all the likes for the post
    likes = likes_schema.dump(post.likes)

    # Return the likes in JSON format
    return {"message": "Likes retrieved successfully", "data": likes}
