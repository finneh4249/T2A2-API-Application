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
    profile_picture : str
        URL of the user's profile picture.
    bio : str
        User's bio.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    profile_picture = db.Column(db.String(), nullable=True)
    bio = db.Column(db.String(500), nullable=True)

    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    posts = db.relationship('Post', back_populates='author')
    likes = db.relationship('Like', back_populates='user')


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
    """
    posts = fields.List(fields.Nested('PostSchema', exclude=['author']))

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

        fields = ('id', 'username', 'email', 'password_hash', 'profile_picture',
                  'bio', 'is_admin', 'is_confirmed', 'confirmed_on', 'posts')


profile_schema = UserSchema(exclude=['password_hash'])
user_schema = UserSchema(
    exclude=['password_hash', 'email', 'is_admin', 'is_confirmed', 'confirmed_on', 'posts'])
users_schema = UserSchema(many=True, exclude=[
                          'password_hash', 'email', 'is_admin', 'is_confirmed', 'confirmed_on', 'posts'])
