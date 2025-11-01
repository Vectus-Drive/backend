from flask import Flask, request
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
from azure.storage.blob import BlobServiceClient
import os, uuid

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

    connect_str = os.getenv('AZURE_CONN_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = 'data'

    API_URL = '/static/api.yaml' 
    SWAGGER_URL = '/api/docs'

    swaggerui_blueprint = get_swaggerui_blueprint(
      SWAGGER_URL,
      API_URL, 
      config={ 
         "app_name": "RPS"
      }
   )

   #* Disable strict slashes globally to enforce cors properly
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

    @app.post('/api/v1/upload-image/')
    def upload_image():
      try:
         uid = request.args.get("uid")

         if 'image' not in request.files:
            return {"error": "No image part"}, HTTP_400_BAD_REQUEST
         
         file = request.files['image']
         if file.filename == '':
            return {"error": "No selected file"}, HTTP_400_BAD_REQUEST
         
         if not uid:
            uid = uuid.uuid4().hex

         _, ext =  file.filename.rsplit(".", 1)
         filename = f"{uid}.{ext}" 
         
         # Upload to Azure Blob Storage
         blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
         blob_client.upload_blob(file, overwrite=True)

         return {"image_url": blob_client.url}, HTTP_201_CREATED
      
      except Exception as e:
         return {
            "status": "error",
            "message": "Failed to upload image",
            "data": None
        }, HTTP_500_INTERNAL_SERVER_ERROR


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