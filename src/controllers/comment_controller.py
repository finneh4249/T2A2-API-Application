"""
This module contains the API endpoints for comment-related operations.

The endpoints are:

- **GET /posts/{post_id}/comments**: Get all comments for a post.
- **POST /posts/{post_id}/comments**: Create a new comment for a post.
- **GET /comments/{comment_id}**: Get a comment by ID.
- **PUT /comments/{comment_id}**: Update a comment.
- **DELETE /comments/{comment_id}**: Delete a comment.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from init import db
from models.comment import Comment, comment_schema, comments_schema
from models.post import Post

comment_controller = Blueprint(
    'comment_controller', __name__, url_prefix='/posts/<int:post_id>/comments')


@comment_controller.route('/', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    """
    Gets a list of all comments on a post.

    Parameters
    ----------
    post_id : int
        The ID of the post to get comments for.

    Returns
    -------
    list of Comment
        A list of all comments on the post.
    """
    # Get the page and per_page parameters from the request
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Get the comments for the post
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc())

    # If there are no comments, return a 404 error
    if not comments:
        return {"message": "No comments found"}, 404

    # Paginate the comments
    paginated_comments = comments.paginate(page=page, per_page=per_page, error_out=False)

    # Dump the comments to a list of dictionaries
    comment_arr = comments_schema.dump(paginated_comments.items)

    # Return the comments
    return {"message": "Comments retrieved successfully", "data": comment_arr}


@comment_controller.route('/', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    """
    Creates a new comment on a post.

    Parameters
    ----------
    post_id : int
        The ID of the post to comment on.

    Request body must contain the following JSON keys:

    - `content`: The content of the comment.

    Returns a JSON representation of the newly created comment.
    """
    post = Post.query.get(post_id)
    if not post:
        # If the post does not exist, return a 404 error
        return {"message": "Post not found"}, 404

    content = request.json['content']
    # Create a new comment with the given content and the current user
    new_comment = Comment(
        user_id=get_jwt_identity(), 
        post_id=post_id, 
        content=content, 
        created_at=datetime.now()
        )
    db.session.add(new_comment)
    db.session.commit()

    # Return the newly created comment in JSON format
    return comment_schema.dump(new_comment)


@comment_controller.route('/<comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(post_id, comment_id):
    """
    Deletes a comment.

    Parameters
    ----------
    post_id : int
        The ID of the post the comment belongs to.

    comment_id : int
        The ID of the comment to delete.

    Returns
    -------
    Comment
        The comment that was deleted.
    """
    # Get the post to ensure it exists
    post = Post.query.get(post_id)
    if not post:
        # If the post does not exist, return a 404 error
        return {"message": "Post not found"}, 404

    # Get the comment to ensure it exists
    comment = Comment.query.get(comment_id)
    if not comment:
        # If the comment does not exist, return a 404 error
        return {"message": "Comment not found"}, 404

    # Check if the user is authorized to delete the comment
    if comment.user_id != get_jwt_identity():
        # If the user is not authorized, return a 401 error
        return {"message": "Unauthorized"}, 401

    # Delete the comment
    db.session.delete(comment)
    db.session.commit()

    # Return the deleted comment in JSON format
    return comment_schema.dump(comment)


@comment_controller.route('/<comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(post_id, comment_id):
    """
    Updates a comment.

    Parameters
    ----------
    post_id : int
        The ID of the post the comment belongs to.

    comment_id : int
        The ID of the comment to update.

    Returns
    -------
    Comment
        The updated comment.
    """
    # Get the post to ensure it exists
    post = Post.query.get(post_id)
    if not post:
        # If the post does not exist, return a 404 error
        return {"message": "Post not found"}, 404

    # Get the comment to ensure it exists
    comment = Comment.query.get(comment_id)
    if not comment:
        # If the comment does not exist, return a 404 error
        return {"message": "Comment not found"}, 404

    # Check if the user is authorized to edit the comment
    if comment.user_id != get_jwt_identity():
        # If the user is not authorized, return a 401 error
        return {"message": "You can only edit your own comments"}, 401

    # Get the data from the request body
    data = request.json

    # Check if the content is different to the existing content
    if data['content'] == comment.content:
        # If the content is the same, return a 400 error
        return {"message": "Comment content must be different to existing content."}, 400

    # Update the comment
    comment.content = data['content']
    db.session.commit()

    # Return the updated comment in JSON format
    return comment_schema.dump(comment)


@comment_controller.route('/<comment_id>', methods=['GET'])
@jwt_required()
def get_comment(post_id, comment_id):
    """
    Gets a specific comment.

    Parameters
    ----------
    post_id : int
        The ID of the post the comment belongs to.

    comment_id : int
        The ID of the comment to get.

    Returns
    -------
    Comment
        The comment with the specified ID.
    """
    # Get the post to ensure it exists
    post = Post.query.get(post_id)
    if not post:
        # If the post does not exist, return a 404 error
        return {"message": "Post not found"}, 404

    # Get the comment to ensure it exists
    comment = Comment.query.get(comment_id)
    if not comment:
        # If the comment does not exist, return a 404 error
        return {"message": "Comment not found"}, 404

    # Return the comment in JSON format
    return comment_schema.dump(comment)
