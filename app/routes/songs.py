from flask import (
    Blueprint
)

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/song', methods=["GET"])
def get_song():
    pass

@bp.route('/song', methods=["POST"])
def create_song():
    pass

@bp.route('/song', methods=["PATCH"])
def update_song():
    pass

@bp.route('/song', methods=["DELETE"])
def delete_song():
    pass
