"""
"""

from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Comment(db.Model):
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
    Schema for serializing and deserializing Like objects.

    Attributes
    ----------
    id : int
        Unique identifier for the like.
    user_id : int
        ID of the user who liked the post.
    post_id : int
        ID of the post that was liked.
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
        model : Like
            The model to serialize.
        """
        fields = ('id', 'user_id', 'post_id', 'content', 'created_at', 'updated_at')

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
