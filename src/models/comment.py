"""
This module contains the Comment model and its associated schema.

The Comment model represents a comment in the database.
"""

from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Comment(db.Model):
    """
    Represents a comment in the database.

    Attributes
    ----------
    id : int
        Unique identifier for the comment.
    user_id : int
        ID of the user who wrote the comment.
    post_id : int
        ID of the post the comment belongs to.
    content : str
        Content of the comment.
    created_at : datetime
        Date and time the comment was created.
    updated_at : datetime
        Date and time the comment was last updated.

    Relationships
    -------------
    user : User
        The user who wrote the comment.
    post : Post
        The post the comment belongs to.
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

class CommentSchema(ma.Schema):
    """
    Schema for serializing and deserializing Comment objects.

    Attributes
    ----------
    id : int
        Unique identifier for the comment.
    user_id : int
        ID of the user who wrote the comment.
    post_id : int
        ID of the post the comment belongs to.
    content : str
        Content of the comment.
    created_at : datetime
        Date and time the comment was created.
    updated_at : datetime
        Date and time the comment was last updated.
    """
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    post_id = fields.Integer(required=True)
    content = fields.String(required=True, validate=Regexp(r'^.{1,500}$'))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        """
        Additional options for the schema.

        Attributes
        ----------
        model : Comment
            The model to serialize.
        """
        fields = ('id', 'user_id', 'post_id', 'content', 'created_at', 'updated_at')

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
