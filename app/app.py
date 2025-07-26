from flask import (
    Flask, 
    )

from .database import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    from .routes import songs
    app.register_blueprint(songs.bp)

    from .routes import instrument_loops
    app.register_blueprint(instrument_loops.bp)

    from .routes import notes
    app.register_blueprint(notes.bp)

    return app