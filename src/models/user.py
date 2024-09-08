"""
This module contains the User model and its associated schema.

The User model represents a user in the database. It contains
attributes for the user's id, username, email, password hash,
profile picture URL, and bio.

The UserSchema is a Marshmallow schema used to serialize and
deserialize the User model.
"""
from marshmallow import fields
from marshmallow.validate import Regexp

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
    profile_picture = db.Column(db.String(), nullable=False)
    bio = db.Column(db.String(500))

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

    class Meta:
        fields = ('id', 'username', 'email', 'password_hash', 'profile_picture', 'bio')

    username = fields.String(required=True, validate=Regexp(r'^[a-zA-Z0-9_]+$'))
    email = fields.Email(required=True)
    password_hash = fields.String(required=True)
    profile_picture = fields.String()
    bio = fields.String()

user_schema = UserSchema(exclude=('password_hash'))
users_schema = UserSchema(many=True, exclude=('password_hash'))