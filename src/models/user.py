"""
This module contains the User model and its associated schema.

The User model represents a user in the database. It contains
attributes for the user's id, username, email, password hash,
profile picture URL, and bio.

The UserSchema is a Marshmallow schema used to serialize and
deserialize the User model.
"""
from marshmallow import fields, validates, ValidationError
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

    profile_picture = db.Column(db.String(), nullable=True)
    bio = db.Column(db.String(500), nullable=True)

    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

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
        """
        Configuration for the UserSchema.

        Attributes
        ----------
        fields : tuple
            The fields to include in the serialized representation of the User.
        """

        fields = ('id', 'username', 'email', 'password_hash', 'profile_picture', 'bio', 'is_admin', 'is_confirmed', 'confirmed_on')

    @validates('username')
    def validate_username(self, username):
        """
        Validates that the username is unique.

        Parameters
        ----------
        username : str
            The username to validate.

        Returns
        -------
        str
            The validated username.

        Raises
        ------
        ValidationError
            If the username is not unique.
        """
        user = User.query.filter_by(username=username).first()
        if user:
            raise ValidationError('Username already exists.')
        return username
    @validates('email')
    def validate_email(self, email):
         # TODO: Add format validation for email
        """
        Validates that the email is unique.

        Parameters
        ----------
        email : str
            The email to validate.

        Returns
        -------
        str
            The validated email.

        Raises
        ------
        ValidationError
            If the email is not unique.
        """
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError('Email already exists.')
        return email

    @validates('password_hash')
    def validate_password(self, password):
        # TODO: Add security validation for password, i.e. at least 8 characters, one uppercase letter, one number, one special character
        """
        Validates that the password is at least 8 characters long.

        Parameters
        ----------
        password : str
            The password to validate.

        Returns
        -------
        str
            The validated password.

        Raises
        ------
        ValidationError
            If the password is less than 8 characters long.
        """
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return password
       


profile_schema = UserSchema(exclude=['password_hash'])
user_schema = UserSchema(exclude=['password_hash', 'email', 'is_admin', 'is_confirmed', 'confirmed_on'])
users_schema = UserSchema(many=True, exclude=['password_hash', 'email', 'is_admin', 'is_confirmed', 'confirmed_on'])

