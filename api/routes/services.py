from flask import Blueprint, request, make_response
from ..database import db
from ..models import Service
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *

service_bp = Blueprint("service", __name__, url_prefix="/api/v1/services")


@service_bp.post("/")
@jwt_required()
def add_service():
    return {'message': 'add service'}, HTTP_200_OK

@service_bp.get("/")
def get_services():
    return {'message': 'get service list'}, HTTP_200_OK

@service_bp.get("/<id>")
def get_service(id):
    return {'message': 'get service by id'}, HTTP_200_OK

@service_bp.delete("/<id>")
@jwt_required()
def delete_service(id):
    return {'message': 'delete service'}, HTTP_200_OK

@service_bp.put("/<id>")
@jwt_required(id)
def update_service():
    return {'message': 'updated service'}, HTTP_200_OK


