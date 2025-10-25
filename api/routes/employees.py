from flask import Blueprint, request, make_response
from ..database import db
from ..models import User
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..utils.helpers import validate_request, validate_response
from ..schemas import EmployeeCreate, EmployeeResponse


employee_bp = Blueprint("employee", __name__, url_prefix="/api/v1/employees")

@employee_bp.get("/")
@jwt_required()
@validate_response(response_model=EmployeeResponse)
def get_employees():
    users = db.session.query(User).filter_by(role="employee").all()

    if not users:
        return {
            "status": "error",
            "message": "No employees registered",
            "data": []
        }, HTTP_404_NOT_FOUND
    
    def handleUser(user):
        employee = user.employee.as_dict()
        user = user.as_dict()

        del employee["employee_id"]
        del user["password"]

        employee["user"] = user

        return employee

    resp_data = [handleUser(user) for user in users]
    
    return {
        "status": "success",
        "message": f"{len(resp_data)} employees found",
        "data": resp_data
    }, HTTP_200_OK

@employee_bp.get("/<id>")
@jwt_required()
@validate_response(response_model=EmployeeResponse)
def get_employee(id):
    user = db.session.query(User).filter_by(u_id=id).first()

    if not user:
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND
    
    employee = user.employee.as_dict()
    user = user.as_dict()
    del employee["employee_id"]
    del user["password"]

    employee["user"] = user
    resp_data = employee

    return {
        "status": "success",
        "message": "Employee retrieved successfully",
        "data": resp_data
    }, HTTP_200_OK

@employee_bp.put("/<id>")
@jwt_required()
@validate_request(request_model=EmployeeCreate)
@validate_response(response_model=EmployeeResponse)
def update_employee(id):
    user = db.session.query(User).filter_by(u_id=id).first()

    if user is None or user.role != "employee" or user.employee is None:
        return {
            "status": "error",
            "message": "Employee does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    data = request.get_json()

    employee_ = user.employee
    employee_.address = data["address"]
    employee_.email = data["email"]
    employee_.image = data["image"]
    employee_.name = data["name"]
    employee_.nic = data["nic"]
    employee_.telephone_no = data["telephone_no"]

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e)
        }, HTTP_500_INTERNAL_SERVER_ERROR

    employee = user.employee.as_dict()
    user = user.as_dict()

    del employee["employee_id"]
    del user["password"]
    
    employee["user"] = user
    resp_data = employee

    return {
        "status": "success",
        "message": "Employee updated successfully",
        "data": resp_data
    }, HTTP_200_OK


