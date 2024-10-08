"""
This module contains the API endpoints for post-related operations.

The endpoints are:

- **GET /posts**: Get a list of all posts.
- **GET /posts/{post_id}**: Get a post by ID.
- **POST /posts**: Create a new post.
- **PUT /posts/{post_id}**: Update a post.
- **DELETE /posts/{post_id}**: Delete a post.

"""

from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from utils import admin_required
from models.post import Post, post_schema, posts_schema
from .comment_controller import comment_controller
from .like_controller import like_controller


post_controller = Blueprint('post_controller', __name__, url_prefix='/posts')

post_controller.register_blueprint(comment_controller)
post_controller.register_blueprint(like_controller)


@post_controller.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_all_posts():
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


@post_controller.route('/<int:post_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_post(post_id):
    """
    Gets a post by ID.

    Parameters
    ----------
    post_id : int
        The ID of the post to retrieve.

    Returns
    -------
    Post
        The post with the given ID.
    """
    post = Post.query.get(post_id)
    if not post:
        return {"message": "Post not found"}, 404
    post_arr = post_schema.dump(post)
    return {"message": "Post retrieved successfully", "data": post_arr}


@post_controller.route('/', methods=['POST'])
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

    new_post = Post(title=title, content=content,
                    created_at=datetime.now(), author_id=get_jwt_identity())
    db.session.add(new_post)
    db.session.commit()

    return post_schema.dump(new_post)


@post_controller.route('/<int:post_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_post(post_id):
    """
    Updates a post in the database.

    Parameters
    ----------
    post_id : int
        The ID of the post to update.

    Returns
    -------
    Post
        The updated post.
    """
    post = Post.query.get(post_id)
    if not post:
        return {"message": "Post not found"}, 404

    if post.author_id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401

    data = request.json

    post.title = data['title'] or post.title
    post.content = data['content'] or post.content
    post.updated_at = datetime.now()

    db.session.commit()

    return post_schema.dump(post)


@post_controller.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """
    Deletes a post from the database.

    Parameters
    ----------
    post_id : int
        The ID of the post to delete.

    Returns
    -------
    dict
        A message indicating the status of the deletion.
    """
    post = Post.query.get(post_id)
    if not post:
        return {"message": "Post not found"}, 404

    if post.author_id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401

    db.session.delete(post)
    db.session.commit()

    return {"message": "Post deleted successfully"}
