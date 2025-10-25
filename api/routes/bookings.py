from flask import Blueprint, request, make_response
from ..database import db
from ..models import Booking
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..schemas import BookingCreate
from pydantic import ValidationError


booking_bp = Blueprint("booking", __name__, url_prefix="/api/v1/bookings")


@booking_bp.post("/")
@jwt_required()
def add_booking():
    return {'message': 'add booking'}, HTTP_200_OK

@booking_bp.get("/")
def get_bookings():
    return {'message': 'get booking list'}, HTTP_200_OK

@booking_bp.get("/<id>")
def get_booking(id):
    return {'message': 'get booking by id'}, HTTP_200_OK

@booking_bp.delete("/<id>")
@jwt_required(id)
def delete_booking():
    return {'message': 'delete booking'}, HTTP_200_OK

@booking_bp.put("/<id>")
@jwt_required(id)
def update_booking():
    return {'message': 'updated booking'}, HTTP_200_OK


