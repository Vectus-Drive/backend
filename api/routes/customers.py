from flask import Blueprint, request, make_response
from ..database import db
from ..models import Customer
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *

customer_bp = Blueprint("customer", __name__, url_prefix="/api/v1/customers")


@customer_bp.post("/")
@jwt_required()
def add_customer():
    return {'message': 'add customer'}, HTTP_200_OK

@customer_bp.get("/")
def get_customers():
    return {'message': 'get customer list'}, HTTP_200_OK

@customer_bp.get("/<id>")
def get_customer(id):
    return {'message': 'get customer by id'}, HTTP_200_OK

@customer_bp.delete("/<id>")
@jwt_required()
def delete_customer(id):
    return {'message': 'delete customer'}, HTTP_200_OK

@customer_bp.put("/<id>")
@jwt_required(id)
def update_customer():
    return {'message': 'updated customer'}, HTTP_200_OK


