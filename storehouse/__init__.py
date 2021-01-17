import os
import ssl
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import app_config

login_manager = LoginManager()

def create_app(environment='development'):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[os.getenv('FLASK_CONFIG', environment)])
    app.config.from_pyfile('application.conf', silent=True)

    from storehouse.models import db

    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        
        # Create all the database objects
        db.create_all()

        from storehouse.views import admin, auth, api
        app.register_blueprint(admin)
        app.register_blueprint(auth)
        app.register_blueprint(api)

    return app