from flask import Blueprint, request
from ..database import db
from ..models import User
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..utils.helpers import validate_request, validate_response
from ..schemas import CustomerCreate, CustomerResponse

customer_bp = Blueprint("customer", __name__, url_prefix="/api/v1/customers")


@customer_bp.get("/")
@jwt_required()
@validate_response(response_model=CustomerResponse)
def get_customers():
    users = db.session.query(User).filter_by(role="customer").all()

    if not users:
        return {
            "status": "error",
            "message": "No customers registered",
            "data": [],
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
        "data": resp_data,
    }, HTTP_200_OK


@customer_bp.get("/<id>")
@jwt_required()
@validate_response(response_model=CustomerResponse)
def get_customer(id):
    user = db.session.query(User).filter_by(u_id=id).first()

    if not user or user.role != "customer":
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None,
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
        "data": resp_data,
    }, HTTP_200_OK


@customer_bp.put("/<id>")
@jwt_required()
@validate_request(request_model=CustomerCreate)
@validate_response(response_model=CustomerResponse)
def update_customer(id):
    user = db.session.query(User).filter_by(u_id=id).first()

    if user is None or user.role != "customer" or user.customer is None:
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None,
        }, HTTP_404_NOT_FOUND

    data = request.get_json()
    image_ = data["image"] if "image" in data else None

    customer_ = user.customer
    customer_.address = data["address"]
    customer_.email = data["email"]
    customer_.image = image_
    customer_.name = data["name"]
    customer_.nic = data["nic"]
    customer_.telephone_no = data["telephone_no"]

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    customer = user.customer.as_dict()
    user = user.as_dict()

    del customer["customer_id"]
    del user["password"]

    customer["user"] = user
    resp_data = customer

    return {
        "status": "success",
        "message": "Customer updated successfully",
        "data": resp_data,
    }, HTTP_200_OK
