from flask import Blueprint, request, make_response
from ..database import db
from ..models import Car
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..schemas import CarCreate
from pydantic import ValidationError

car_bp = Blueprint("car", __name__, url_prefix="/api/v1/cars")

@car_bp.post("/")
def create_car():
    try:
        data = request.json
        car = CarCreate.model_validate(data)
    except ValidationError as e:
        return {
            "status": "error",
            "message": "Invalid input",
            "data": e.errors()[0]
        }, HTTP_400_BAD_REQUEST

    pass

@car_bp.get("/")
def get_cars():
    cars = db.session.query(Car).all()

    if not cars:
        return {
            "status": "error",
            "message": "No cars registered",
            "data": []
        }, HTTP_404_NOT_FOUND

    data = [car.as_dict() for car in cars]
    return {
        "status": "success",
        "message": f"{len(data)} cars found",
        "data": data
    }, HTTP_200_OK

@car_bp.get("/<id>")
def get_car(id):
    car = db.session.query(Car).filter_by(car_id=id).first()

    if not car:
        return {
            "status": "error",
            "message": "car does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    return {
        "status": "success",
        "message": "car retrieved successfully",
        "data": car.as_dict()
    }, HTTP_200_OK


@car_bp.delete("/<id>")
@jwt_required(id)
def delete_car():
    car = db.session.query(Car).filter_by(car_id=id).first()

    if not car:
        return {
            "status": "error",
            "message": "car does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    car.delete(synchronize_session=False)
    db.commit()

    # REST convention: 204 No Content, empty response
    return '', HTTP_204_NO_CONTENT

@car_bp.put("/<id>")
@jwt_required(id)
def update_car():
    car_query = db.session.query(Car).filter_by(car_id=id)

    if car_query.first() is None:
        return {
            "status": "error",
            "message": "car does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND
    
    try:
        data = request.json
        car = CarCreate.model_validate(data)
    except ValidationError as e:
        return {
            "status": "error",
            "message": "Invalid input",
            "data": e.errors()[0]
        }, HTTP_400_BAD_REQUEST

    data['car_id'] = id

    updated_car = car_query.update(data, synchronize_session=False)
    db.session.commit()

    return {
        "status": "success",
        "message": "car updated successfully",
        "data": car.model_dump()
    }, HTTP_200_OK
