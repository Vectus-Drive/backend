from flask import Blueprint, request, make_response
from ..database import db
from ..models import Employee
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..schemas import EmployeeCreate
from pydantic import ValidationError


employee_bp = Blueprint("employee", __name__, url_prefix="/api/v1/employees")

@employee_bp.get("/")
def get_employees():
    employees = db.session.query(Employee).all()
    if not employees:
        return {
            "status": "error",
            "message": "No employees registered",
            "data": []
        }, HTTP_404_NOT_FOUND

    data = [employee.as_dict() for employee in employees]
    return {
        "status": "success",
        "message": f"{len(data)} employees found",
        "data": data
    }, HTTP_200_OK

@employee_bp.get("/<id>")
def get_employee(id):
    employee = db.session.query(Employee).filter_by(employee_id=id).first()

    if not employee:
        return {
            "status": "error",
            "message": "Employee does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    return {
        "status": "success",
        "message": "Employee retrieved successfully",
        "data": employee.as_dict()
    }, HTTP_200_OK

@employee_bp.delete("/<id>")
@jwt_required()
def delete_employee(id):
    employee = db.session.query(Employee).filter_by(employee_id=id).first()

    if not employee:
        return {
            "status": "error",
            "message": "Employee does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    employee.delete(synchronize_session=False)
    db.commit()

    # REST convention: 204 No Content, empty response
    return '', HTTP_204_NO_CONTENT

@employee_bp.put("/<id>")
@jwt_required(id)
def update_employee():
    employee_query = db.session.query(Employee).filter_by(employee_id=id)

    if employee_query.first() is None:
        return {
            "status": "error",
            "message": "Employee does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND
    
    try:
        data = request.json
        employee = EmployeeCreate.model_validate(data)
    except ValidationError as e:
        return {
            "status": "error",
            "message": "Invalid input",
            "data": e.errors()[0]
        }, HTTP_400_BAD_REQUEST

    data['employee_id'] = id

    updated_employee = employee_query.update(data, synchronize_session=False)
    db.session.commit()

    return {
        "status": "success",
        "message": "Employee updated successfully",
        "data": employee.model_dump()
    }, HTTP_200_OK


