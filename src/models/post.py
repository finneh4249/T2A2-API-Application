"""
This module contains the Post model and its associated schema.

The Post model represents a post in the database.
"""
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Regexp

from init import db, ma


class Post(db.Model):
    """
    Represents a post in the database.

    Attributes
    ----------
    id : int
        Unique identifier for the post.
    title : str
        Title of the post.
    content : str
        Content of the post.
    author_id : int
        ID of the user who created the post.
    created_at : datetime
        Date and time the post was created.
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    author = db.relationship('User', back_populates='posts')
    likes = db.relationship('Like', back_populates='post')


class PostSchema(ma.Schema):
    """
    Schema for serializing and deserializing Post objects.

    Attributes
    ----------
    id : int
        Unique identifier for the post.
    title : str
        Title of the post.
    content : str
        Content of the post.
    created_at : datetime
        Date and time the post was created.
    author_id : int
        ID of the user who created the post.
    """

    id = fields.Integer()
    author = fields.Nested('UserSchema', only=['id', 'username'])
    title = fields.String(required=True, validate=Regexp(r'^.{1,80}$'))
    content = fields.String(required=True, validate=Regexp(r'^.{1,500}$'))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    likes = fields.List(fields.Nested('LikeSchema', exclude=['post_id']))

    likes_count = fields.Method(serialize="get_likes_count")

    # TODO: Add like count to the schema based on the number of likes a post has
    # like_count = fields.Integer(dump_only=True)

    class Meta:
        """
        Configuration for the PostSchema.

        Attributes
        ----------
        fields : tuple
            The fields to include in the serialized representation of the Post.
        """

        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author', 'likes', 'likes_count')

    def get_likes_count(self, post, **kwargs):
        """
        Returns the number of likes a post has.
    
        Parameters
        ----------
        post : Post
            The post to get the like count for.
    
        Returns
        -------
        int
            The number of likes the post has.
        """
        return len(post.likes)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

