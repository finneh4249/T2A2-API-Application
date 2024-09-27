"""
This module contains a Blueprint for the CLI commands.

The commands are:

- `db_create`: Create all tables in the database.
- `db_drop`: Drop all tables in the database.
- `create_user <username> <email> <password> <bio> [--admin]`: Create a user, use the --admin flag to create an admin user.
- `delete_user <username>`: Delete the selected user from the database.

"""

import click
from flask import Blueprint
from datetime import datetime

from init import db, bcrypt
from models.user import User
from models.post import Post
from models.like import Like
from models.comment import Comment
from models.follow import Follow

from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError


cli_controller = Blueprint('cli', __name__)

@cli_controller.cli.command("create_user")
@click.argument("username", default="user")
@click.argument("email", default="user@localhost")
@click.argument("password", default="user")
@click.argument("bio", default="This is a user.")
@click.option("--admin", is_flag=True)
def create_user(username, email, password, admin):
    """
    Creates a user in the database.

    The user is created with the specified username, email address,
    password, and admin status.
    """
    # Hash the password
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
    # Create a new user with the given information
    user = User(username=username, email=email, password_hash=hash_password, bio=bio,
                is_admin=admin, is_confirmed=True, confirmed_on=datetime.now())
    # Add the new user to the database
    db.session.add(user)
    db.session.commit()


@cli_controller.cli.command("db_create")
def create_tables():
    """
    Creates all tables in the database.
    """
    db.create_all()
    print("Tables created successfully.\n")
    users = [
        User(username="admin", email="admin@localhost", password_hash=bcrypt.generate_password_hash(
            "admin").decode('utf-8'), is_admin=True, is_confirmed=True, confirmed_on=datetime.now()),
        User(username="user", email="user@localhost", password_hash=bcrypt.generate_password_hash(
            "user").decode('utf-8'), is_admin=False, is_confirmed=True, confirmed_on=datetime.now())
    ]
    db.session.add_all(users)

    posts = [
        Post(title="Hello, World!", content="This is my first post. Created by the Admin!",
             author=users[0], created_at=datetime.now()),
        Post(title="Another Post", content="This is my second post. Created by the User",
             author=users[1], created_at=datetime.now())
    ]
    db.session.add_all(posts)

    likes = [
        Like(user=users[0], post=posts[1]),
        Like(user=users[1], post=posts[0])
    ]
    db.session.add_all(likes)

    comments = [
        Comment(user=users[0], post=posts[1],
                content="This is a comment on the second post.", created_at=datetime.now()),
        Comment(user=users[1], post=posts[0],
                content="This is a comment on the first post.", created_at=datetime.now())
    ]
    db.session.add_all(comments)

    follows = [
        Follow(follower=users[0], follows=users[1]),
        Follow(follower=users[1], follows=users[0])
    ]
    db.session.add_all(follows)
    db.session.commit()
    print("User data added successfully.",
          "\n\nDefault users:\nadmin:admin\nuser:user\n\n",
          "You can use these credentials to login.",
          "\nYou can create new users using the 'create_user' command.",
          "\nIf you encounter an error and need to reset the database, use the 'db_reset' command.")


@cli_controller.cli.command("db_drop")
def drop_tables():
    """
    Drops all tables in the database.
    """
    db.drop_all()
    print("Tables dropped successfully.")


@cli_controller.cli.command("delete_user")
@click.argument("username")
def delete_user(username):
    """
    Deletes a user from the database.

    The user is deleted with the given username.
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        print(f"User '{username}' does not exist.")
        return
    db.session.delete(user)
    try:
        db.session.commit()
        print(f"User '{username}' deleted successfully.")
    except (IntegrityError, OperationalError, DatabaseError) as e:
        db.session.rollback()
        print(f"Database error: {e}")
