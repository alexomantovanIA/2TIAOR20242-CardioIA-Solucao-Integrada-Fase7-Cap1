import os
import logging
from flask import Flask, jsonify, request, send_from_directory, g

from backend.config import Config
from backend.routes.chat_routes import chat_bp
from backend.routes.integration_routes import integration_bp
from backend.routes.prediction_routes import prediction_bp
from backend.utils.auth import AuthError, parse_jwt_without_signature, validate_entra_claims

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    app.register_blueprint(chat_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(integration_bp)

    @app.before_request
    def protect_api_routes():
        if not app.config.get("AUTH_ENABLED", True):
            return None

        if request.method == "OPTIONS":
            return None
        if request.path == "/health":
            return None
        if not request.path.startswith("/api/"):
            return None

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Unauthorized: token ausente."}), 401

        token = auth_header.replace("Bearer ", "", 1).strip()
        try:
            claims = parse_jwt_without_signature(token)
            g.user = validate_entra_claims(
                claims,
                tenant_id=app.config["ENTRA_TENANT_ID"],
                audience=app.config["ENTRA_AUDIENCE"],
                issuer=app.config["ENTRA_ISSUER"],
            )
        except AuthError as exc:
            return jsonify({"message": f"Unauthorized: {exc}"}), 401

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = Config.CORS_ORIGINS
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

    @app.route("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/<path:filename>")
    def frontend_files(filename):
        frontend_path = os.path.join(FRONTEND_DIR, filename)
        if os.path.isfile(frontend_path):
            return send_from_directory(FRONTEND_DIR, filename)

        assets_path = os.path.join(ASSETS_DIR, filename)
        if os.path.isfile(assets_path):
            return send_from_directory(ASSETS_DIR, filename)

        return send_from_directory(FRONTEND_DIR, filename)

    @app.route("/assets/<path:filename>")
    def asset_files(filename):
        return send_from_directory(ASSETS_DIR, filename)

    return app


if __name__ == "__main__":
    app = create_app()
    mode = "Watson Assistant" if Config.watson_configured() else "Fallback Local"
    logger.info("CardioIA iniciando em modo: %s", mode)
    logger.info("Acesse: http://localhost:%s", Config.PORT)
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
