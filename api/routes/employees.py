from flask import Blueprint, request, make_response
from ..database import db
from ..models import Employee
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *

employee_bp = Blueprint("employee", __name__, url_prefix="/api/v1/employees")


@employee_bp.post("/")
@jwt_required()
def add_employee():
    return {'message': 'add employee'}, HTTP_200_OK

@employee_bp.get("/")
def get_employees():
    return {'message': 'get employee list'}, HTTP_200_OK

@employee_bp.get("/<id>")
def get_employee(id):
    return {'message': 'get employee by id'}, HTTP_200_OK

@employee_bp.delete("/<id>")
@jwt_required()
def delete_employee(id):
    return {'message': 'delete employee'}, HTTP_200_OK

@employee_bp.put("/<id>")
@jwt_required(id)
def update_employee():
    return {'message': 'updated employee'}, HTTP_200_OK


