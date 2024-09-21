"""
Provides utility functions for the application.

This module contains functions that are used throughout the application,
but do not fit into any particular category.

"""
from functools import wraps

from flask_jwt_extended import get_jwt_identity
from flask import abort

from models.user import User

def admin_required(fn):
    """
    Checks if the current user has admin priviliges before executing
    the decorated function.

    :param fn: The function to be decorated
    :return: The decorated function
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
       
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            abort(403)
        return fn(*args, **kwargs)
    return decorated_function
