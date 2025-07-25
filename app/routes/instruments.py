from flask import Blueprint

bp = Blueprint('instrument', __name__, url_prefix='/instrument')

@bp.route('/', methods=["GET"])
def get_instrument():
    pass

@bp.route('/', methods=["POST"])
def create_instrument():
    pass

@bp.route('/<id>', methods=["PATCH"])
def update_instrument():
    pass

@bp.route('/<id>', methods=["DELETE"])
def delete_instrument():
    pass