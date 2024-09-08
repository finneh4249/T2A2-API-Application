from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

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
