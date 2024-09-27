"""
Represents a like in the database.

A like is a connection between a user and a post where the user has
expressed that they like the post. A like can be thought of as a
"vote" for a post, saying that the user liked the post.

Attributes
----------
id : int
    Unique identifier for the like.
user_id : int
    ID of the user who liked the post.
post_id : int
    ID of the post that was liked.
created_at : datetime
    Date and time the like was created.

"""

from init import db, ma
from marshmallow import fields


class Like(db.Model):
    """
    Represents a like in the database.

    A like is a connection between a user and a post where the user has
    expressed that they like the post.

    Attributes
    ----------
    id : int
        Unique identifier for the like.
    user_id : int
        ID of the user who liked the post.
    post_id : int
        ID of the post that was liked.

    Relationships
    -------------
    user : User
        The user who liked the post.
    post : Post
        The post that was liked.

    """
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')


class LikeSchema(ma.Schema):
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

    class Meta:
        """
        Additional options for the schema.

        Attributes
        ----------
        model : Like
            The model to serialize.
        """
        fields = ('id', 'user_id', 'post_id')


like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)
