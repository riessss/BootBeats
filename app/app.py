from flask import (
    Flask, 
    render_template
    )

def create_app():
    app = Flask(__name__)

    from sqlalchemy.orm import DeclarativeBase
    class Base(DeclarativeBase):
        pass
    
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(model_class=Base)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    from .routes import songs
    app.register_blueprint(songs.bp)

    from .routes import instruments
    app.register_blueprint(instruments.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    

    return app, db