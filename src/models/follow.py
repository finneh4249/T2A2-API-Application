"""
This module contains the Follow model and its associated schema.

The Follow model represents a follow in the database. It contains
attributes for the id, follower_id, and followed_id.

The FollowSchema is a Marshmallow schema used to serialize and
deserialize the Follow model.
"""
from init import db, ma
from marshmallow import fields


class Follow(db.Model):
    """
    Represents a follow in the database.

    Attributes
    ----------
    id : int
        Unique identifier for the follow.
    follower_id : int
        ID of the user who is following another user.
    followed_id : int
        ID of the user who is being followed.

    Relationships
    -------------
    follower : User
        The user who is following another user.
    follows : User
        The user who is being followed.
    """

    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    follower = db.relationship('User', foreign_keys=[follower_id])
    follows = db.relationship('User', foreign_keys=[followed_id])


class FollowSchema(ma.Schema):
    """
    Schema for serializing and deserializing Follow objects.

    Attributes
    ----------
    id : int
        Unique identifier for the follow.
    follower_id : int
        ID of the user who is following another user.
    followed_id : int
        ID of the user who is being followed.
    """

    id = fields.Integer(dump_only=True)
    follower_id = fields.Integer(required=True)
    followed_id = fields.Integer(required=True)

    class Meta:
        """
        Additional options for the schema.

        Attributes
        ----------
        model : Follow
            The model to serialize.
        """
        fields = ('id', 'follower_id', 'followed_id')


follow_schema = FollowSchema()
follows_schema = FollowSchema(many=True)
