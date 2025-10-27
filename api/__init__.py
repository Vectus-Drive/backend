from flask import Flask, redirect
from .config import Config
from .database import db
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from .utils.http_status_codes import *
# from .models import User, Booking, Car, Customer, Review,  Token, Transaction, Service
from .services.auth import auth_bp
from .routes.cars import car_bp
from .routes.customers import customer_bp
from .routes.reviews import review_bp
from .routes.bookings import booking_bp
from .routes.transactions import transaction_bp
from .routes.services import service_bp
from .routes.employees import employee_bp

def create_app():
    app = Flask(__name__)
    CORS(
   app, 
   origins=["http://localhost:5173"],
   supports_credentials=True,
   # allow_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN"]
   
)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
      db.create_all()

    jwt = JWTManager()
    jwt.init_app(app)
    
    API_URL = '/static/api.yaml' 
    SWAGGER_URL = '/api/docs'

    swaggerui_blueprint = get_swaggerui_blueprint(
      SWAGGER_URL,
      API_URL, 
      config={ 
         "app_name": "RPS"
      }
   )
    
    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(auth_bp)
    app.register_blueprint(car_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(employee_bp)

    
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
       return {
          "error" : "Not found"
       }, HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
       return {
          "error" : "Something went wrong please try again"
       }, HTTP_500_INTERNAL_SERVER_ERROR
    
    
    return app
