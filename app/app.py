from flask import (
    Flask, 
    render_template
    )

from database import db

def create_app():
    app = Flask(__name__)
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