"""
This module contains the User model and its associated schema.

The User model represents a user in the database. It contains
attributes for the user's id, username, email, password hash,
profile picture URL, and bio.

The UserSchema is a Marshmallow schema used to serialize and
deserialize the User model.
"""
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Regexp, And, Length

from init import db, ma


class User(db.Model):
    """
    Represents a user in the database.

    Attributes
    ----------
    id : int
        Unique identifier for the user.
    username : str
        Username chosen by the user. Must be unique.
    email : str
        Email associated with the user.
    password_hash : str
        Hashed password for the user.
    bio : str
        User's bio.
    is_admin : bool
        If the user is an admin.
    is_confirmed : bool
        If the user has confirmed their email.
    confirmed_on : datetime
        The datetime the user confirmed their email.
    posts : list[Post]
        The posts the user has made.
    likes : list[Like]
        The likes the user has made.
    comments : list[Comment]
        The comments the user has made.
    follows : list[Follow]
        The users the user is following.
    followers : list[Follow]
        The users that are following the user.

    Notes
    -----
    The relationships are defined as follows:
    - A user can make many posts.
    - A user can make many likes.
    - A user can make many comments.
    - A user can follow many users.
    - A user can be followed by many users.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    bio = db.Column(db.String(500), nullable=True)

    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    posts = db.relationship('Post', back_populates='author')
    likes = db.relationship('Like', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')

    follows = db.relationship(
        'Follow', foreign_keys='Follow.followed_id', back_populates='follows')
    followers = db.relationship(
        'Follow', foreign_keys='Follow.follower_id', back_populates='follower')


class UserSchema(ma.Schema):
    """
    Schema for serializing and deserializing User objects.

    Attributes
    ----------
    id : int
        Unique identifier for the user.
    username : str
        Username chosen by the user. Must be unique.
    email : str
        Email associated with the user.
    password_hash : str
        Hashed password for the user.
    profile_picture : str
        URL of the user's profile picture.
    bio : str
        User's bio.
    is_admin : bool
        If the user is an admin.
    is_confirmed : bool
        If the user has confirmed their email.
    confirmed_on : datetime
        The datetime the user confirmed their email.
    posts : list[Post]
        The posts the user has made.
    likes : list[Like]
        The likes the user has made.
    comments : list[Comment]
        The comments the user has made.
    followers : list[Follow]
        The users that are following the user.
    follows : list[Follow]
        The users the user is following.
    likes_count : int
        The number of likes the user has made.
    followers_count : int
        The number of users following the user.
    following_count : int
        The number of users the user is following.
    """
    posts = fields.List(fields.Nested(
        'PostSchema', exclude=['author', 'likes', 'comments']))
    likes = fields.List(fields.Nested('LikeSchema', exclude=['user_id']))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user_id']))
    followers = fields.List(fields.Nested(
        'FollowSchema', exclude=['followed_id']))
    follows = fields.List(fields.Nested(
        'FollowSchema', exclude=['follower_id']))

    likes_count = fields.Method(serialize="get_likes_count")
    followers_count = fields.Method(serialize="get_followers_count")
    following_count = fields.Method(serialize="get_following_count")

    email = fields.String(required=True, validate=Regexp(
        r"^\S+@\S+\.S+$", error="Invalid email format"))
    password_hash = fields.String(required=True, validate=Regexp(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", error="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number"))
    username = fields.String(required=True, validate=And(Length(min=4, max=100, error="Username must be between 4 and 100 characters"), Regexp(
        r"^[a-zA-Z0-9 ]+$", error="Username must contain only alphanumeric characters")))

    class Meta:

        """
        Configuration for the UserSchema.

        Attributes
        ----------
        fields : tuple
            The fields to include in the serialized representation of the User.
        """

        fields = ('id', 'username', 'email', 'password_hash', 
                'profile_picture', 'bio', 
                'likes_count', 'followers_count', 'following_count', 
                'is_admin', 'is_confirmed', 'confirmed_on',
                'posts', 'likes', 'comments', 
                'followers', 'follows')


    def get_likes_count(self, user, **kwargs):
        """
        Returns the number of likes a user has.

        This method is used as a field in the UserSchema to
        include the number of likes a user has in the serialized
        representation of the user.

        Parameters
        ----------
        user : User
            The user to get the like count for.

        Returns
        -------
        int
            The number of likes the user has.
        """
        # Get the number of likes the user has
        return len(user.likes) or 0

    def get_followers_count(self, user, **kwargs):
        """
        Returns the number of followers a user has.

        Parameters
        ----------
        user : User
            The user to get the follower count for.

        Returns
        -------
        int
            The number of followers the user has.
        """
        # Get the number of followers the user has using a query
        return len(user.followers) or 0
    def get_following_count(self, user, **kwargs):
        """
        Returns the number of users the given user is following.

        Parameters
        ----------
        user : User
            The user to get the following count for.

        Returns
        -------
        int
            The number of users the given user is following.
        """
        # Get the number of users the user is following
        return len(user.follows) or 0


profile_schema = UserSchema(exclude=['password_hash'])
user_schema = UserSchema(only=('id', 'username', 'email'))
users_schema = UserSchema(many=True, only=('id', 'username', 'email'))
