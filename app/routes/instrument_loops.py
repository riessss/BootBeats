from flask import Blueprint, request, jsonify
from sqlalchemy import select, func

from ..models import InstrumentLoop
from ..database import db

bp = Blueprint('instrument', __name__, url_prefix='/instrument')


@bp.route('/add_instrument', methods=['POST'])
def add_instrument():
    data = request.get_json()
    song_id = data.get('song_id')
    instrument_id = data.get('instrument_id')

    
    if not song_id or not instrument_id:
        return jsonify(success=False, error="Missing song_id or instrument_id"), 400
    
    loop_count = db.session.execute(
        select(func.count(InstrumentLoop.id)).where(InstrumentLoop.song_id == song_id)
        ).scalar_one()


    if loop_count > 4:
        return {"error": "Need at least one instrument"}, 400
        
    loop = InstrumentLoop(
        song_id=song_id,
        instrument_id=instrument_id,
        notes=["C5", "B5"]
    )
    db.session.add(loop)
    db.session.commit()
    return {
        "success": True,
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
    return {
        "success": True,
        "message": "Instrument deleted"
        }, 200
