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
from flask_login import login_required, current_user

from .models import Song, InstrumentLoop, User, db

bp = Blueprint('songs', __name__, url_prefix='/')

@login_required
@bp.route('/')
def redirect_first_song():
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        return redirect('/auth/login')
    print("User:", current_user.id, current_user.is_authenticated)
    song = Song.query.filter(Song.user_id == user_id).first()
    print("Song found:", song)
    return redirect(url_for('.index', user_id=user_id, song_id=song.id))


@login_required
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


@login_required
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

@login_required
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


@login_required
@bp.route('/<int:loop_id>', methods=["POST"])
def update_notes(loop_id):
    notes_string = request.form.get('notes', '')
    notes_list = notes_string.split(', ')

    loop = db.get_or_404(InstrumentLoop, loop_id)

    loop.notes = notes_list
    db.session.commit()
    return redirect(url_for('songs.index',
                            song_id=loop.song_id))


@bp.route('/change_title/<int:song_id>', methods=["PATCH"])
def update_title(song_id):
    song = db.get_or_404(Song, song_id)
    
    data = request.get_json()
    new_title = data.get('title')
    
    song.title = new_title
    db.session.commit()

    return {"data":{
        "song_id": song_id,
        "title": new_title
    }}