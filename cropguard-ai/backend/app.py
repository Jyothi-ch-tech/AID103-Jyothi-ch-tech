from flask import Flask
from flask_cors import CORS
import os

# Import blueprints
from controllers.user_controller import user_bp
from controllers.predict_controller import predict_bp
from controllers.farm_controller import farm_bp
from controllers.alerts_controller import alerts_bp
from controllers.admin_controller import admin_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(predict_bp, url_prefix="/api")
app.register_blueprint(farm_bp, url_prefix="/api")
app.register_blueprint(alerts_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

@app.route("/")
def home():
    return {"status": "CropGuard AI Backend Running", "version": "1.0"}

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
