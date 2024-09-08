from flask import Blueprint

from init import db
from models.user import User




cli_controller = Blueprint('cli', __name__)


@cli_controller.cli.command("create_admin")
def create_admin():
    """
    Creates an admin user in the database.

    The admin user is created with username "admin", email
    address "admin@localhost", and password "admin".
    """
    admin = User(username="admin", email="admin@localhost", password_hash="admin")
    db.session.add(admin)
    db.session.commit()


@cli_controller.cli.command("create_user")
def create_user():
    """
    Creates a user in the database.

    The user is created with username "user", email
    address "user@localhost", and password "user".
    """
    user = User(username="user", email="user@localhost", password_hash="user")
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
    