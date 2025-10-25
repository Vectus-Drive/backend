from flask import Blueprint, request
from ..database import db
from ..models import Customer, User
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..utils.helpers import validate_request, validate_response
from ..schemas import CustomerCreate, CustomerResponse, CustomerResponseList

customer_bp = Blueprint("customer", __name__, url_prefix="/api/v1/customers")

@customer_bp.get("/")
@jwt_required()
@validate_response(response_model=CustomerResponseList)
def get_customers():
    users = db.session.query(User).all()

    if not users:
        return {
            "status": "error",
            "message": "No customers registered",
            "data": []
        }, HTTP_404_NOT_FOUND
    
    def handleUser(user):
        customer = user.customer.as_dict()
        user = user.as_dict()

        del customer["customer_id"]
        del user["password"]

        customer["user"] = user

        return customer

    resp_data = [handleUser(user) for user in users]
    
    return {
        "status": "success",
        "message": f"{len(resp_data)} customers found",
        "data": resp_data
    }, HTTP_200_OK


@customer_bp.get("/<id>")
@jwt_required()
@validate_response(response_model=CustomerResponse)
def get_customer(id):
    user = db.session.query(User).filter_by(u_id=id).first()

    if not user:
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND
    
    customer = user.customer.as_dict()
    user = user.as_dict()
    del customer["customer_id"]
    del user["password"]

    customer["user"] = user
    resp_data = customer

    return {
        "status": "success",
        "message": "Customer retrieved successfully",
        "data": resp_data
    }, HTTP_200_OK


@customer_bp.delete("/<id>")
@jwt_required()
def delete_customer(id):
    customer = db.session.query(Customer).filter_by(customer_id=id).first()

    if not customer:
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    customer.delete(synchronize_session=False)
    db.commit()

    # REST convention: 204 No Content, empty response
    return '', HTTP_204_NO_CONTENT


@customer_bp.put("/<id>")
@jwt_required()
@validate_request(request_model=CustomerCreate)
@validate_response(response_model=CustomerResponse)
def update_customer(id):
    user = db.session.query(User).filter_by(u_id=id).first()

    if user is None:
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND
    
    data = request.get_json()

    customer_ = user.customer
    customer_.address = data["address"]
    customer_.email = data["email"]
    customer_.image = data["image"]
    customer_.name = data["name"]
    customer_.nic = data["nic"]
    customer_.telephone_no = data["telephone_no"]

    db.session.commit()

    customer = user.customer.as_dict()
    user = user.as_dict()

    del customer["customer_id"]
    del user["password"]
    
    customer["user"] = user
    resp_data = customer

    return {
        "status": "success",
        "message": "Customer updated successfully",
        "data": resp_data
    }, HTTP_200_OK
