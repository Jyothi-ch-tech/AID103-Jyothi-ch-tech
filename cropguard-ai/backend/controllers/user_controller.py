from flask import Blueprint, request, jsonify
try:
    from ..models.user import create_user, verify_user
except ImportError:
    from models.user import create_user, verify_user

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    mode = data.get("mode", "register")
    email = data.get("email", "")
    password = data.get("password", "")
    name = data.get("name", "")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    if mode == "login":
        ok = verify_user(email, password)
        if not ok:
            return jsonify({"error": "invalid credentials"}), 401
        return jsonify({"status": "ok", "email": email})
    created = create_user(email, password, name)
    if created is None:
        return jsonify({"error": "user exists"}), 409
    return jsonify({"status": "ok", "email": email, "user": created})
