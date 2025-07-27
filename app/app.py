from flask import (
    Flask,
    render_template
    )

from .database import db
from .models import Song, Instrument, InstrumentLoop


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    from .router import bp
    app.register_blueprint(bp)
    
    @app.route('/test')
    def test_db():
    # Query the database
        songs = Song.query.all()
        instruments = Instrument.query.all()
        loops = InstrumentLoop.query.all()

        # Return everything as JSON
        return {
            "songs": [s.title for s in songs],
            "instruments": [i.name for i in instruments],
            "loops": [(l.id, l.notes) for l in loops]
        }

    return app