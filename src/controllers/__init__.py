from flask import Blueprint

auth_controller = Blueprint('auth_controller', __name__, url_prefix='/auth')
user_controller = Blueprint('user_controller', __name__, url_prefix='/users')
cli_controller = Blueprint('cli_controller', __name__, url_prefix='/cli')
post_controller = Blueprint('post_controller', __name__, url_prefix='/posts')
feed_controller = Blueprint('feed_controller', __name__, url_prefix='/feed')
like_controller = Blueprint('like_controller', __name__, url_prefix='/<int:post_id>')
comment_controller = Blueprint('comment_controller', __name__, url_prefix='/<int:post_id>')

post_controller.register_blueprint(like_controller)
post_controller.register_blueprint(comment_controller)
