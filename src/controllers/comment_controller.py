
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

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)


    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc())
    if not comments:
        return {"message": "No comments found"}, 404

    paginated_comments = comments.paginate(page=page, per_page=per_page, error_out=False)

    comment_arr = comments_schema.dump(paginated_comments.items)
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
        return {"message": "Post not found"}, 404

    content = request.json['content']

    new_comment = Comment(
        user_id=get_jwt_identity(), 
        post_id=post_id, 
        content=content, 
        created_at=datetime.now()
        )
    db.session.add(new_comment)
    db.session.commit()

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
    post = Post.query.get(post_id)
    if not post:
        return {"message": "Post not found"}, 404

    comment = Comment.query.get(comment_id)
    if not comment:
        return {"message": "Comment not found"}, 404

    if comment.user_id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401

    db.session.delete(comment)
    db.session.commit()

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
    post = Post.query.get(post_id)
    if not post:
        return {"message": "Post not found"}, 404

    comment = Comment.query.get(comment_id)
    if not comment:
        return {"message": "Comment not found"}, 404

    if comment.user_id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401

    data = request.json

    comment.content = data['content'] or comment.content

    db.session.commit()

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
    post = Post.query.get(post_id)
    if not post:
        return {"message": "Post not found"}, 404

    comment = Comment.query.get(comment_id)
    if not comment:
        return {"message": "Comment not found"}, 404

    return comment_schema.dump(comment)
