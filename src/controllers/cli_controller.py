"""
This module contains the CLI controller for the Flask application.

The CLI controller contains functions that are decorated with the
@cli_controller.cli.command() decorator. These functions are used to
create database tables and users.

"""
import click
from flask import Blueprint
from datetime import datetime

from init import db, bcrypt
from models.user import User
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError


cli_controller = Blueprint('cli', __name__)


@cli_controller.cli.command("create_user")
@click.argument("username", default="user")
@click.argument("email", default="user@localhost")
@click.argument("password", default="user")
@click.option("--admin", is_flag=True)
def create_user(username, email, password, admin):
    """
    Creates a user in the database.

    The user is created with the specified username, email address,
    password, and admin status.
    """
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password_hash=hash_password,
                is_admin=admin, is_confirmed=True, confirmed_on=datetime.now())
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
    db.session.commit()
    print("User data added successfully.\n\nDefault users:\nadmin:admin\nuser:user\n\nYou can use these credentials to login.\nYou can create new users using the 'create_user' command.\nIf you encounter an error and need to reset the database, use the 'db_reset' command.")


@cli_controller.cli.command("db_drop")
def drop_tables():
    """
    Drops all tables in the database.
    """
    db.drop_all()
    print("Tables dropped successfully.")


@cli_controller.cli.command("db_reset")
def reset_tables():
    """
    Resets all tables in the database.
    """
    drop_tables()
    create_tables()
    print("Tables reset successfully.")


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
