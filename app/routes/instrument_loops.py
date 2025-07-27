from flask import Blueprint, jsonify, redirect, url_for
from sqlalchemy import select, func
import base64

from ..models import InstrumentLoop
from ..database import db

bp = Blueprint('instrument', __name__, url_prefix='/instrument')


@bp.route('/add_instrument/<int:instrument_id>/<int:song_id>', methods=['POST', 'GET'])
def add_instrument(instrument_id, song_id):

    if not song_id or not instrument_id:
        return jsonify(success=False, error="Missing song_id or instrument_id"), 400
    
    loop_count = db.session.execute(
        select(func.count(InstrumentLoop.id)).where(InstrumentLoop.song_id == song_id)
    ).scalar_one()

    if loop_count > 5:
        return {"error": "No more than 6 instruments"}, 400
    
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
        return {"error": "Need at least one instrument"}, 400
    
    loop = db.get_or_404(InstrumentLoop, loop_id)

    db.session.delete(loop)
    db.session.commit()

    return redirect(url_for('songs.index', 
                    song_id=song_id))
