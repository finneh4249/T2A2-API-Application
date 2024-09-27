"""
This module contains the feed controller, which handles the retrieval of
posts for a user's feed.

The feed is a list of posts that are visible to the user. This includes
posts from users that the user is following, as well as the user's own
posts.

The endpoints are:

- **GET /feed**: Get a list of all posts in the database in chronological order.
- **GET /feed/following**: Get a list of all posts from users the current user is following.

"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.post import Post, posts_schema

feed_controller = Blueprint('feed_controller', __name__, url_prefix='/feed')


@feed_controller.route('/', methods=['GET'])
@jwt_required()
def get_feed():
    """
    Retrieves a list of all posts in the database.

    The posts are paginated and can be navigated using the following query
    parameters:

    - `page`: The page to retrieve. Defaults to 1.
    - `per_page`: The number of posts to retrieve per page. Defaults to 10.

    Returns
    -------
    list of Post
        A list of all posts in the database.
    """
    # Get the page number from the request query parameters, default to 1
    page = request.args.get('page', 1, type=int)

    # Get the number of posts to retrieve per page from the request query
    # parameters, default to 10
    per_page = request.args.get('per_page', 10, type=int)

    # Retrieve all posts from the database
    posts = Post.query.order_by(Post.created_at.desc())

    # Paginate the posts
    paginated_posts = posts.paginate(
        page=page, per_page=per_page, error_out=False)

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
    user_id = get_jwt_identity()

    # Get all of the users the current user is following
    follows = Follow.query.filter_by(follower_id=user_id).all()

    # Get the page number from the request query parameters, default to 1
    page = request.args.get('page', 1, type=int)

    # Get the number of posts to retrieve per page from the request query
    # parameters, default to 10
    per_page = request.args.get('per_page', 10, type=int)

    # Create a list of all the user IDs the current user is following
    followed_ids = [follow.followed_id for follow in follows]

    # If user is not following anyone, return an empty list
    if not followed_ids:
        return {"message": "No posts found from followed users"}, 200

    # Retrieve all posts from users in the followed list
    posts = Post.query.filter(Post.user_id.in_(
        followed_ids)).order_by(Post.created_at.desc())

    # Paginate the posts
    paginated_posts = posts.paginate(
        page=page, per_page=per_page, error_out=False)

    # Serialize the paginated posts
    post_arr = posts_schema.jsonify(paginated_posts.items)

    # Return the serialized posts
    return post_arr
