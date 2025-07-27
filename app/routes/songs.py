from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template
)

from ..models import Song, InstrumentLoop, db

bp = Blueprint('songs', __name__, url_prefix='/')

@bp.route('/')
def redirect_first_song():
    first_song = Song.query.first()
    return redirect(url_for('.index', song_id=first_song.id))


@bp.route('/<int:song_id>')
def index(song_id):
    song = db.get_or_404(Song, song_id)

    used_instruments_ids = []
    instrument_loops = []
    for instrument_loop in song.instrument_loops:
        used_instruments_ids.append(instrument_loop.instrument_id)
        loop_data = {
            "id": instrument_loop.id,
            "instrument_id": instrument_loop.instrument_id,
            "notes": instrument_loop.notes
        } 
                
        instrument_loops.append(loop_data)

        instrument_icons = {
            1: "🎹 Piano",
            2: "🥁 Drums",
            3: "🎸 Guitar",
            4: "🎸 Bass",      
            5: "🎶 Flute",    
            6: "🎻 Violin",
            7: "🎺 Trumpet"
        }


    return render_template('index.html',
                           song=song,
                           instrument_loops=instrument_loops,
                           instrument_icons=instrument_icons,
                           used_instruments_ids=used_instruments_ids)



