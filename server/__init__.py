from flask import Flask, jsonify, request
from flask_cors import CORS
from server.routes import auth, v1
from server.extensions import db, chroma_client, limiter, login_manager, logger
from server.config import CONFIG
from server.models.Users import USER
from server.models.Subscriptions import SUBSCRIPTIONS
from jsonschema.exceptions import SchemaError


def create_app(*args, **kwargs):
    logger.info("Creating App")
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    app.config.from_object(CONFIG)
    db.init_app(app)
    chroma_collection = chroma_client.create_collection(name=CONFIG.CHROMA_COLLECTION)
    login_manager.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return USER.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "Unauthorized"}), 401

    @app.before_request
    def log_request_info():
        logger.info(f"Method: {request.method}")
        logger.info(f"URL: {request.url}")
        logger.info(f"Headers: {request.headers}")
        logger.info(f"Body: {request.get_data()}")

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({"error": "Method Not Allowed"}), 405

    @app.errorhandler(401)
    def handle_unauthorized(e):
        return jsonify({"error": "Unauthorized Access"}), 401

    app.register_blueprint(auth)
    app.register_blueprint(v1)

    return app
