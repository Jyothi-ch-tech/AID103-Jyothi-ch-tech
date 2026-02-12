from flask import Blueprint, request, jsonify
try:
    from ..models.alert import get_alerts
except ImportError:
    from models.alert import get_alerts

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/alerts", methods=["GET"])
def alerts():
    email = request.args.get("email")
    items = get_alerts(email)
    return jsonify({"alerts": items})
