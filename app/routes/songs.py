from flask import (
    Blueprint,
    jsonify,
    request
)

from ..models import Song, InstrumentLoop
from ..database import db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/song/<int:song_id>', methods=["GET"])
def get_song(song_id):
    song = db.get_or_404(Song, song_id)
    return jsonify({"id": song.id,
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
                    ]}), 200

@bp.route('/song', methods=["POST"])
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
    

@bp.route('/song/<int:song_id>', methods=["DELETE"])
def delete_song(song_id):
    song = Song
    db.session.delete(song)
    db.session.commit()
    return {"message": "Deleting succesfull!"}, 200
