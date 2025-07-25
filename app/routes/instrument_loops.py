from flask import Blueprint

from ..models import InstrumentLoop
from ..database import db

bp = Blueprint('instrument', __name__, url_prefix='/instrument')


@bp.route('/<int:song_id>/<int:instrument_id>', methods=["POST"])
def create_instrument(song_id, instrument_id):
    loop = InstrumentLoop(
        song_id=song_id,
        instrument_id=instrument_id)
    
    db.session.add(loop)
    db.session.commit()
    return {
        "id": loop.id,
        "song_id": loop.song_id,
        "instrument_id": loop.instrument_id
    }, 201




@bp.route('/<id>', methods=["DELETE"])
def delete_instrument():
    pass