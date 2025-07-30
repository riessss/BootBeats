from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from .database import db
from .models import User

login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .auth import auth
    app.register_blueprint(auth)

    from .router import bp
    app.register_blueprint(bp)
    
    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    
    login_manager.login_view = '/auth/login'
  
    return app