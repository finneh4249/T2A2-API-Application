"""

"""
from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from utils import admin_required
from models.post import Post, post_schema, posts_schema


post_controller = Blueprint('post_controller', __name__, url_prefix='/posts')


@post_controller.route('/', methods=['GET'])
@jwt_required()
@admin_required
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

@post_controller.route('/create', methods=['POST'])
@jwt_required()
def create_post():
    """
    Creates a new post in the database.

    Request body must contain the following JSON keys:

    - `title`: The title of the post.
    - `content`: The content of the post.

    Returns a JSON representation of the newly created post.
    """
    title = request.json['title']
    content = request.json['content']

    new_post = Post(title=title, content=content, created_at=datetime.now(), author_id=get_jwt_identity())
    db.session.add(new_post)
    db.session.commit()

    return post_schema.dump(new_post)