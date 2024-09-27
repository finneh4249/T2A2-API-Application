"""
This module contains the Post model and its associated schema.

The Post model represents a post in the database. It contains
attributes for the post's id, title, content, author_id, created_at,
and updated_at.

The PostSchema is a Marshmallow schema used to serialize and
deserialize the Post model.
"""
from marshmallow import fields
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
    updated_at : datetime
        Date and time the post was last updated.

    Relationships
    -------------
    author : User
        The user who created the post.
    comments : list[Comment]
        The comments on the post.
    likes : list[Like]
        The likes on the post.
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
    comments = db.relationship('Comment', back_populates='post')
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
    comments = fields.List(fields.Nested('CommentSchema', exclude=['post_id']))
    likes = fields.List(fields.Nested('LikeSchema', exclude=['post_id']))

    likes_count = fields.Method(serialize="get_likes_count")
    comments_count = fields.Method(serialize="get_comments_count")

    class Meta:
        """
        Configuration for the PostSchema.

        Attributes
        ----------
        fields : tuple
            The fields to include in the serialized representation of the Post.
        """

        fields = ('id', 'title', 'content', 'likes_count', 'comments_count',
                  'created_at', 'updated_at', 'author', 'likes', 'comments')

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

    def get_comments_count(self, post, **kwargs):
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
        return len(post.comments)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
