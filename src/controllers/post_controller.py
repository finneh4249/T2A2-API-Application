"""

"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.post import Post, post_schema, posts_schema

post_controller = Blueprint('post_controller', __name__, url_prefix='/posts')


@post_controller.route('/', methods=['GET'])
@jwt_required()
def get_posts():
    """
    Gets a list of all posts in the database.

    Returns
    -------
    list of Post
        A list of all posts in the database.
    """
    posts = Post.query.all()
    post_arr = posts_schema.dump(posts)
    return {"message": "Posts retrieved successfully", "data": post_arr}