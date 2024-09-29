"""
This module contains all the controllers for the application.

The controllers are:

- `auth_controller`: Handles authentication and authorization.
- `user_controller`: Handles user-related operations.
- `cli_controller`: Handles CLI-related operations.
- `post_controller`: Handles post-related operations.
- `comment_controller`: Handles comment-related operations.
- `like_controller`: Handles like-related operations.
- `feed_controller`: Handles feed-related operations.
- `follow_controller`: Handles follow-related operations.

"""

from .auth_controller import auth_controller as auth
from .user_controller import user_controller as user
from .cli_controller import cli_controller as cli
from .post_controller import post_controller as post
from .feed_controller import feed_controller as feed