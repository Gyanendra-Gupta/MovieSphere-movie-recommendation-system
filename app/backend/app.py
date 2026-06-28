from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import DevelopmentConfig
from models import db, bcrypt

# Import Blueprints
from routes.auth import auth_bp
from routes.movies import movies_bp
from routes.user_data import user_data_bp

# Inside backend/app.py or config.py
# Initialize Extensions
jwt = JWTManager()
migrate = Migrate()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Enable CORS
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True
    )

    # ---------------------------
    # Home Route
    # ---------------------------
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "MovieSphere API is running",
            "status": "success"
        }), 200

    # ---------------------------
    # Register Blueprints
    # ---------------------------
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(movies_bp, url_prefix="/api/movies")
    app.register_blueprint(user_data_bp, url_prefix="/api/user")

    # ---------------------------
    # Error Handlers
    # ---------------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": "Internal Server Error"
        }), 500

    return app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )