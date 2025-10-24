from flask import Blueprint, request
from ..database import db
from ..models import Customer
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..schemas import CustomerCreate
from pydantic import ValidationError

customer_bp = Blueprint("customer", __name__, url_prefix="/api/v1/customers")

@customer_bp.get("/")
@jwt_required()
def get_customers():
    customers = db.session.query(Customer).all()

    if not customers:
        return {
            "status": "error",
            "message": "No customers registered",
            "data": []
        }, HTTP_404_NOT_FOUND

    data = [customer.as_dict() for customer in customers]
    return {
        "status": "success",
        "message": f"{len(data)} customers found",
        "data": data
    }, HTTP_200_OK


@customer_bp.get("/<id>")
@jwt_required()
def get_customer(id):
    customer = db.session.query(Customer).filter_by(customer_id=id).first()

    if not customer:
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    return {
        "status": "success",
        "message": "Customer retrieved successfully",
        "data": customer.as_dict()
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
def update_customer(id):
    customer_query = db.session.query(Customer).filter_by(customer_id=id)

    if customer_query.first() is None:
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND
    
    try:
        data = request.json
        customer = CustomerCreate.model_validate(data)
    except ValidationError as e:
        return {
            "status": "error",
            "message": "Invalid input",
            "data": e.errors()[0]
        }, HTTP_400_BAD_REQUEST

    data['customer_id'] = id

    updated_customer = customer_query.update(data, synchronize_session=False)
    db.session.commit()

    return {
        "status": "success",
        "message": "Customer updated successfully",
        "data": customer.model_dump()
    }, HTTP_200_OK
