from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    jsonify,
    flash
)
from sqlalchemy import select, func

from .models import Song, InstrumentLoop, db

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
            "notes": instrument_loop.notes,
            "instrument_name": instrument_loop.instrument.name
        } 
                
        instrument_loops.append(loop_data)

    instrument_icons = {
        1: "🎹 Piano",
        2: "🥁 Drums",
        3: "🪕 Guitar",
        4: "💥 Reverse Bass",         
        5: "🎼 Flute",        
        6: "🎻 Violin",
        7: "🔔 Hi-Hat",          
    }


    return render_template('index.html',
                           song=song,
                           instrument_loops=instrument_loops,
                           instrument_icons=instrument_icons,
                           used_instruments_ids=used_instruments_ids)


@bp.route('/add_instrument/<int:instrument_id>/<int:song_id>', methods=['POST', 'GET'])
def add_instrument(instrument_id, song_id):

    if not song_id or not instrument_id:
        return jsonify(success=False, error="Missing song_id or instrument_id"), 400
    
    loop_count = db.session.execute(
        select(func.count(InstrumentLoop.id)).where(InstrumentLoop.song_id == song_id)
    ).scalar_one()

    if loop_count == 6:
        flash("Not more than 6 instruments allowed!", "error")
        return redirect(url_for('songs.index', 
                    song_id=song_id))
    
    loop = InstrumentLoop(instrument_id=instrument_id, 
                          song_id=song_id,
                          notes=["C5", "B5"])

    db.session.add(loop)
    db.session.commit()
        

    return redirect(url_for('songs.index', 
                    song_id=song_id))


@bp.route('/<int:song_id>/<int:loop_id>', methods=["POST", "GET"])
def delete_instrument(song_id, loop_id):
    loop_count = db.session.scalar(
        select(func.count(InstrumentLoop.id))
        .where(InstrumentLoop.song_id == song_id)
    )

    if loop_count <= 1:
        flash("At least one instrument needed!", "error")
        return redirect(url_for('songs.index', 
                    song_id=song_id))
    
    loop = db.get_or_404(InstrumentLoop, loop_id)

    db.session.delete(loop)
    db.session.commit()

    return redirect(url_for('songs.index', 
                    song_id=song_id))


@bp.route('/<int:loop_id>', methods=["POST"])
def update_notes(loop_id):
    notes_string = request.form.get('notes', '')
    notes_list = notes_string.split(', ')

    loop = db.get_or_404(InstrumentLoop, loop_id)

    loop.notes = notes_list
    db.session.commit()
    return redirect(url_for('songs.index',
                            song_id=loop.song_id))