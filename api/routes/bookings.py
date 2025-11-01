from flask import Blueprint, request, make_response
from ..database import db
from ..models import Booking, Customer, Car
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..utils.helpers import generate_booking_id, validate_request, validate_response
from ..schemas import BookingCreate, BookingResponse, BookingUpdate


booking_bp = Blueprint("booking", __name__, url_prefix="/api/v1/bookings")


@booking_bp.post("/")
@jwt_required()
def add_booking():
    data = request.get_json()
    customer_id = data["customer_id"]
    car_id = data["car_id"]

    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if not customer:
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND
    
    car = Car.query.filter_by(car_id=car_id).first()
    if not car:
        return {
            "status": "error",
            "message": "Car does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    booking_id = generate_booking_id()
    data["booking_id"] = booking_id

    booking = Booking(**data)
    db.session.add(booking)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    resp_data = booking.as_dict()

    return {
        "status": "success",
        "message": "Booking created successfully",
        "data": resp_data,
    }, HTTP_201_CREATED

@booking_bp.get("/")
@jwt_required()
@validate_response(response_model=BookingResponse)
def get_bookings():
    customer_id = request.args.get("customer_id")
    car_id = request.args.get("car_id")

    query = db.session.query(Booking)

    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if car_id:
        query = query.filter_by(car_id=car_id)

    bookings = query.all()

    if not bookings:
        return {
            "status": "error",
            "message": "No bookings found",
            "data": [],
        }, HTTP_404_NOT_FOUND

    def handle_booking(booking):
        car = booking.car.as_dict()
        booking = booking.as_dict()

        if customer_id:
            del booking["customer_id"]

        del car["car_id"]
        booking["car"] = car
        return booking

    resp_data = [handle_booking(booking) for booking in bookings]

    return {
        "status": "success",
        "message": f"Found {len(bookings)} bookings",
        "data": resp_data,
    }, HTTP_200_OK


@booking_bp.get("/<id>")
@jwt_required()
@validate_response(response_model=BookingResponse)
def get_booking(id):
    booking = db.session.query(Booking).filter_by(booking_id=id).first()

    if not booking:
        return {
            "status": "error",
            "message": "Booking not found",
            "data": None,
        }, HTTP_404_NOT_FOUND

    car = booking.car.as_dict()
    del car["car_id"]
    resp_data = booking.as_dict()
    resp_data["car"] = car
    
    return {
        "status": "success",
        "message": "Booking retrieved successfully",
        "data": resp_data,
    }, HTTP_200_OK

@booking_bp.delete("/<id>")
@jwt_required()
def delete_booking(id):
    booking = db.session.query(Booking).filter_by(booking_id=id).first()
    if not booking:
        return {
            "status": "error",
            "message": "Booking not found",
            "data": None,
        }, HTTP_404_NOT_FOUND

    db.session.delete(booking)

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

@booking_bp.put("/<id>")
@jwt_required()
@validate_request(request_model=BookingUpdate)
@validate_response(response_model=BookingResponse)
def update_booking(id):
    booking_query = db.session.query(Booking).filter_by(booking_id=id)

    booking = booking_query.first()

    if not booking:
        return {
            "status": "error",
            "message": "Booking not found",
            "data": None,
        }, HTTP_404_NOT_FOUND
    
    customer_id = booking.customer.customer_id
    car = booking.car.as_dict()
    car_id = car["car_id"]

    data = request.get_json()
    data["customer_id"] = customer_id
    data["car_id"] = car_id
    updated_booking= booking_query.update(data, synchronize_session=False)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    del car["car_id"]
    data["booking_id"] = id
    data["car"] = car
    resp_data = data

    return {
        "status": "success",
        "message": "Booking updated successfully",
        "data": resp_data,
    }, HTTP_200_OK


