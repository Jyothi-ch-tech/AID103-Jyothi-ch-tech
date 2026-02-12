from flask import Blueprint, request, jsonify
try:
    from ..utils.image_utils import save_upload
    from ..services.ai_service import infer
    from ..services.recommendation_service import recommend
    from ..services.alert_service import risk_level
    from ..models.alert import create_alert
except ImportError:
    from utils.image_utils import save_upload
    from services.ai_service import infer
    from services.recommendation_service import recommend
    from services.alert_service import risk_level
    from models.alert import create_alert

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    email = request.form.get("email", "")
    crop_type = request.form.get("crop_type", "")
    location = request.form.get("location", "")
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "image required"}), 400
    path, name = save_upload(file)
    res = infer(path)
    rec = recommend(res["disease"], crop_type, res["severity"])
    explanation = "Model indicates " + res["disease"] + " with " + str(res["confidence"]) + "% confidence."
    result = {
        "disease": res["disease"],
        "confidence": res["confidence"],
        "severity": res["severity"],
        "recommendation": rec,
        "explanation": explanation,
        "image": name
    }
    level = risk_level(res["severity"])
    create_alert(email, res["disease"], res["confidence"], level, location)
    return jsonify(result)
