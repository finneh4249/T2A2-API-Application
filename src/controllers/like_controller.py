from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.post import Post, post_schema
from models.like import Like, likes_schema
from models.user import User, user_schema


post_controller = Blueprint('post_controller', __name__, url_prefix='/posts/<int:post_id>')

@post_controller.route('/like', methods=['POST'])
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
        return {"message": "Post not found"}, 404

    user_id = get_jwt_identity()

    if user_id == post.author_id:
        return {"message": "Cannot like own post"}, 400


    if any(like.user_id == user_id for like in post.likes):
        return {"message": "Post already liked"}, 400
    
    # Create a new Like object and add it to the post's likes
    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    message = post_schema.dump(post)

    return message

@post_controller.route('/like', methods=['DELETE'])
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
    post = Post.query.get(post_id)
    if not post:
        return {"message": "Post not found"}, 404

    user_id = get_jwt_identity()


    if not any(like.user_id == user_id for like in post.likes):
        return {"message": "Post not liked"}, 400

    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()

    db.session.delete(like)
    db.session.commit()

    return post_schema.dump(post)

@post_controller.route('/likes', methods=['GET'])
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
    post = Post.query.get(post_id)
    if not post:
        return {"message": "Post not found"}, 404

    likes = likes_schema.dump(post.likes)
    return {"message": "Likes retrieved successfully", "data": likes}