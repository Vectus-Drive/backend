from flask import Blueprint, request, make_response
from ..database import db
from ..models import Car
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *

car_bp = Blueprint("car", __name__, url_prefix="/api/v1/cars")


@car_bp.post("/")
@jwt_required()
def add_car():
    return {'message': 'add car'}, HTTP_200_OK

@car_bp.get("/")
def get_cars():
    return {'message': 'get car list'}, HTTP_200_OK

@car_bp.get("/<id>")
def get_car(id):
    return {'message': 'get car by id'}, HTTP_200_OK

@car_bp.delete("/<id>")
@jwt_required(id)
def delete_car():
    return {'message': 'delete car'}, HTTP_200_OK

@car_bp.put("/<id>")
@jwt_required(id)
def update_car():
    return {'message': 'updated car'}, HTTP_200_OK


