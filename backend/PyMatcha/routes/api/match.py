from flask import Blueprint
from flask import current_app
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.utils.success import SuccessOutput

match_bp = Blueprint("matches", __name__)


@match_bp.route("/matches", methods=["GET"])
@jwt_required
def get_user_matches():
    current_app.logger.debug(f"Getting matches for {current_user.id}")
    return SuccessOutput("matches", [m.to_dict() for m in current_user.get_matches()])
