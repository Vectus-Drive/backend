from flask import Flask, send_from_directory
from .config import Config
from .database import db
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from .utils.http_status_codes import *
from flask_migrate import Migrate
from .services.auth import auth_bp
from .routes.cars import car_bp
from .routes.customers import customer_bp
from .routes.reviews import review_bp
from .routes.bookings import booking_bp
from .routes.transactions import transaction_bp
from .routes.services import service_bp
from .routes.employees import employee_bp
from .routes.notifications import notification_bp
import os


def create_app():
    app = Flask(__name__)
    CORS(
        app,
        origins=["http://localhost:5173"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        supports_credentials=True,
    )
    app.config.from_object(Config)

    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    # TODO: remember to remove db.create_all() once all migrations are stable
    with app.app_context():
        db.create_all()

    jwt = JWTManager()
    jwt.init_app(app)

    API_URL = "/static/api.yaml"
    SWAGGER_URL = "/api/docs"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "RPS"}
    )

    # * Disable strict slashes globally to enforce cors properly
    app.url_map.strict_slashes = False

    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(auth_bp)
    app.register_blueprint(car_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(notification_bp)

    # serve images from the uploads folder
    @app.route("/uploads/<filename>")
    def serve_user_image(filename):
        u_prefix, _ = filename.split("_", 1)
        sub_folder = "users" if u_prefix == "USER" else "cars"

        upload_folder = os.path.join(
            os.path.dirname(__file__), "..", "uploads", sub_folder
        )
        
        return send_from_directory(upload_folder, filename)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return {"error": "Not found"}, HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return {
            "error": "Something went wrong please try again"
        }, HTTP_500_INTERNAL_SERVER_ERROR

    return app