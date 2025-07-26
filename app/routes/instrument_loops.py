from flask import Blueprint
from sqlalchemy import select, func

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


@bp.route('/<int:song_id>/<int:loop_id>', methods=["DELETE"])
def delete_instrument(song_id, loop_id):
    loop_count = db.session.scalar(
        select(func.count(InstrumentLoop.id))
        .where(InstrumentLoop.song_id == song_id)
    )

    if loop_count <= 1:
        return {"error": "Need at least one instrument"}, 400
    
    loop = db.get_or_404(InstrumentLoop, loop_id)

    db.session.delete(loop)
    db.session.commit()
    return {"message": "Instrument deleted"}, 200
