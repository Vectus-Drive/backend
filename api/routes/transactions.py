from flask import Blueprint, request, make_response
from ..database import db
from ..models import Transaction, Booking, Car, Customer
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..utils.helpers import generate_transaction_id, validate_request, validate_response
from ..schemas import TransactionCreate, TransactionResponse, TransactionUpdate


transaction_bp = Blueprint("transaction", __name__, url_prefix="/api/v1/transactions")


@transaction_bp.post("/")
@jwt_required()
@validate_request(request_model=TransactionCreate)
@validate_response(response_model=TransactionResponse)
def add_transaction():
    data = request.get_json()
    booking_id = data["booking_id"]

    booking = Booking.query.filter_by(booking_id=booking_id).first()
    if not booking:
        return {
            "status": "error",
            "message": "Booking does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND
    
    car_id = booking.car.car_id
    customer_id = booking.customer.customer_id
    
    transaction_id = generate_transaction_id()
    data["transaction_id"] = transaction_id
    data["car_id"] = car_id
    data["customer_id"] = customer_id
    
    transaction = Transaction(**data)
    db.session.add(transaction)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    resp_data = transaction.as_dict()

    return {
        "status": "success",
        "message": "Transaction created successfully",
        "data": resp_data,
    }, HTTP_201_CREATED

@transaction_bp.get("/")
def get_transactions():
    customer_id = request.args.get("customer_id")
    car_id = request.args.get("car_id")

    query = db.session.query(Transaction)

    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if car_id:
        query = query.filter_by(car_id=car_id)

    transactions = query.all()

    if not transactions:
        return {
            "status": "error",
            "message": "No transaction records found",
            "data": [],
        }, HTTP_404_NOT_FOUND

    def handle_transaction(transaction):
        if customer_id:
            del transaction["customer_id"]
        if car_id:
            del transaction["car_id"]
        return transaction

    resp_data = [handle_transaction(transaction.as_dict()) for transaction in transactions]

    return {
        "status": "success",
        "message": f"Found {len(transactions)} bookings",
        "data": resp_data,
    }, HTTP_200_OK

@transaction_bp.get("/<id>")
def get_transaction(id):
    transaction = db.session.query(Transaction).filter_by(transaction_id=id).first()

    if not transaction:
        return {
            "status": "error",
            "message": "Transaction record not found",
            "data": None,
        }, HTTP_404_NOT_FOUND

    resp_data = transaction.as_dict()

    return {
        "status": "success",
        "message": "Booking retrieved successfully",
        "data": resp_data,
    }, HTTP_200_OK


@transaction_bp.delete("/<id>")
@jwt_required()
def delete_transaction(id):
    transaction = db.session.query(Transaction).filter_by(transaction_id=id).first()
    if not transaction:
        return {
            "status": "error",
            "message": "Transaction record not found",
            "data": None,
        }, HTTP_404_NOT_FOUND

    db.session.delete(transaction)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    return {}, HTTP_204_NO_CONTENT

@transaction_bp.put("/<id>")
@jwt_required()
@validate_request(request_model=TransactionUpdate)
@validate_response(response_model=TransactionResponse)
def update_transaction(id):
    transaction_query = db.session.query(Transaction).filter_by(transaction_id=id)

    transaction = transaction_query.first()

    if not transaction:
        return {
            "status": "error",
            "message": "Transaction record not found",
            "data": None,
        }, HTTP_404_NOT_FOUND
    
    customer_id = transaction.customer_id
    car_id = transaction.car_id
    data = request.get_json()
    data["customer_id"] = customer_id
    data["car_id"] = car_id
    updated_booking= transaction_query.update(data, synchronize_session=False)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    data["transaction_id"] = id
    resp_data = data

    return {
        "status": "success",
        "message": "Transaction updated successfully",
        "data": resp_data,
    }, HTTP_200_OK


