from flask import Blueprint, request, jsonify
try:
    from ..models.farm import add_farm
except ImportError:
    from models.farm import add_farm

farm_bp = Blueprint("farm", __name__)

@farm_bp.route("/addFarm", methods=["POST"])
def addFarm():
    data = request.get_json() or {}
    email = data.get("email", "")
    crop_type = data.get("crop_type", "")
    sow_date = data.get("sow_date", "")
    location = data.get("location", "")
    if not email or not crop_type or not sow_date:
        return jsonify({"error": "missing fields"}), 400
    res = add_farm(email, crop_type, sow_date, location)
    return jsonify(res)
