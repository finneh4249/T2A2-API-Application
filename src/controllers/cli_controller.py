"""
This module contains the CLI controller for the Flask application.

The CLI controller contains functions that are decorated with the
@cli_controller.cli.command() decorator. These functions are used to
create database tables and users.

"""

from flask import Blueprint

from init import db, bcrypt
from models.user import User


cli_controller = Blueprint('cli', __name__)

   


@cli_controller.cli.command("create_admin")
def create_admin():
    """
    Creates an admin user in the database.

    The admin user is created with username "admin", email
    address "admin@localhost", and password "admin".
    """
    password= "admin"
    hash_password = bcrypt.generarate_password_hash(password.encode('utf-8'))
    admin = User(username="admin", email="admin@localhost", password_hash=hash_password, is_admin=True, is_confirmed=True)
    db.session.add(admin)
    db.session.commit()


@cli_controller.cli.command("create_user")
def create_user():
    """
    Creates a user in the database.

    The user is created with username "user", email
    address "user@localhost", and password "user".
    """
    password= "user"
    hash_password = bcrypt.generarate_password_hash(password.encode('utf-8'))
    user = User(username="user", email="user@localhost", password_hash=hash_password, is_admin=False, is_confirmed=True)
    db.session.add(user)
    db.session.commit()

@cli_controller.cli.command("db_create")
def create_tables():
    """
    Creates all tables in the database.
    """
    db.create_all()


@cli_controller.cli.command("db_drop")
def drop_tables():
    """
    Drops all tables in the database.
    """
    db.drop_all()
