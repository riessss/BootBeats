from flask import (
    Blueprint, 
    request
)

from ..models import InstrumentLoop, Note
from ..database import db

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/<int:loop_id>/notes', methods=["PATCH"])
def update_notes(loop_id):
    data = request.get_json()

    notes = data.get("notes", [])
    loop = db.get_or_404(InstrumentLoop, loop_id)

    loop.notes = notes
    db.session.commit()
    return {
        "message": "Notes updated",
        "notes": loop.notes }, 200