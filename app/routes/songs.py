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

    instrument_loops = []
    for instrument_loop in song.instrument_loops:
        loop_data = {
            "id": instrument_loop.id,
            "instrument_id": instrument_loop.instrument_id,
            "notes": [
                {
                    "id": note.id,
                    "pitch": note.pitch,
                    "start_time": note.start,
                    "duration": note.duration
                }
                for note in instrument_loop.notes
            ]
        }
        instrument_loops.append(loop_data)

        instrument_icons = {
            1: "🎹 Piano",
            2: "🥁 Drums",
            3: "🎸 Guitar",
            4: "🎸 Bass",      # Using guitar emoji for bass (no bass emoji)
            5: "🎶 Flute",     # No flute emoji, using a generic music note
            6: "🎻 Violin",
            7: "🎺 Trumpet"
        }


    return render_template('index.html',
                           song=song,
                           instrument_loops=instrument_loops,
                           instrument_icons=instrument_icons)



def view_song(song_id):
    song = db.get_or_404(Song, song_id)
    return {"id": song.id,
                "title": song.title,
                "tempo": song.tempo,
                "instrument_loops": [
                    {
                        "id": loop.id, 
                        "instrument_id": loop.instrument_id,
                        "notes":[
                            {
                                "id": note.id,
                                "pitch": note.pitch,
                                "start_time": note.start,
                                "duration": note.duration
                            } for note in loop.notes
                        ]
                    } for loop in song.instrument_loops
                ]}, 200

def create_song():
    if request.is_json():
        data = request.get_json()
        title = data.get('title')
        tempo = data.get('tempo')
        
        song = Song(title=title, tempo=tempo)

        piano_loop = InstrumentLoop(name="Piano")
        song.instrument_loops.append(piano_loop)

        db.session.add(song)
        db.session.commit()

        return {
            "id": song.id,
            "title": song.title,
            "tempo": song.tempo,
            "instrument_loops": [
                {
                    "id": piano_loop.id,
                    "instrument_id": piano_loop.instrument_id
                }
            ]
        }, 201
    
def delete_song(song_id):
    # TODO: If last song not possible to delete.
    song = Song
    db.session.delete(song)
    db.session.commit()
    return {"message": "Deleting succesfull!"}, 200
