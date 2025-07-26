from flask import (
    Flask,
    render_template
    )

from .database import db
from .models import Song, Instrument, Note, InstrumentLoop


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    from .routes import songs
    app.register_blueprint(songs.bp)

    from .routes import instrument_loops
    app.register_blueprint(instrument_loops.bp)

    from .routes import notes
    app.register_blueprint(notes.bp)

    @app.route('/')
    def index1():
        return render_template('index.html')
    
    @app.route('/test')
    def test_db():
    # Query the database
        songs = Song.query.all()
        instruments = Instrument.query.all()
        notes = Note.query.all()
        loops = InstrumentLoop.query.all()

        # Return everything as JSON
        return {
            "songs": [s.title for s in songs],
            "instruments": [i.name for i in instruments],
            "notes": [
                {"pitch": n.pitch, "start": n.start, "duration": n.duration}
                for n in notes
            ],
            "loops": [l.id for l in loops]
        }

    return app