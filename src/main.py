import os
from init import db, ma, bcrypt, jwt

from flask import Flask

def create_app()

    app = Flask(__name__)
    app.json.sort_keys = False

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    

    return app