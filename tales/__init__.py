from flask import Flask
from tales.config import Config
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from tales.users.routes import users
    from tales.posts.routes import posts
    from tales.main.routes import main
    from tales.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
