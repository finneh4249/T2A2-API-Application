"""
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from . import feed_controller
from models.post import Post, post_schema, posts_schema

@feed_controller.route('/', methods=['GET'])
@jwt_required()
def get_feed():
    """
    Gets a list of all posts in the database.

    The posts are paginated and can be navigated using the following query
    parameters:

    - `page`: The page to retrieve. Defaults to 1.
    - `per_page`: The number of posts to retrieve per page. Defaults to 10.

    Returns
    -------
    list of Post
        A list of all posts in the database.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Retrieve all posts from the database
    posts = Post.query.order_by(Post.created_at.desc())

    # Paginate the posts
    paginated_posts = posts.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize the paginated posts
    post_arr = posts_schema.jsonify(paginated_posts.items)

    # Return the serialized posts
    return post_arr

@feed_controller.route('/following', methods=['GET'])
@jwt_required()
def get_following_feed():
    """
    Gets a list of all posts from users the current user is following.

    Returns
    -------
    list of Post
        A list of all posts from followed users.
    """
    pass

