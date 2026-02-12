from flask import Blueprint, jsonify
try:
    from ..models.report import get_reports
except ImportError:
    from models.report import get_reports

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/reports", methods=["GET"])
def reports():
    items = get_reports()
    return jsonify({"reports": items})
