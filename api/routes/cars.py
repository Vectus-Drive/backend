from flask import Blueprint, request, make_response
from ..database import db
from ..models import Car
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..utils.helpers import validate_request, validate_response, generate_car_id, save_image_locally, delete_image
from ..schemas import CarCreate, CarResponse

car_bp = Blueprint("car", __name__, url_prefix="/api/v1/cars")

def updateService(service):
    del service["car_id"]
    return service

@car_bp.post("/")
@validate_request(request_model=CarCreate)
@validate_response(response_model=CarResponse)
def create_car():
    data = request.get_json()

    car_id = generate_car_id()
    data["car_id"] = car_id

    try:
        save_image_locally(_id=car_id, source_path=data["image"])
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR


    image_, ext_ = data["image"].rsplit(".", 1)
    data["image"] = f"{car_id}.{ext_}"
    
    car = Car(**data)
    db.session.add(car)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR
    
    resp_data = {
        "car_id": car_id,
        "license_no": data["license_no"],
        "make": data["make"],
        "model": data["model"]
    }

    return {
        "status": "success",
        "message": "Car created successfully",
        "data": resp_data,
    }, HTTP_201_CREATED

@car_bp.get("/")
@validate_response(response_model=CarResponse)
def get_cars():
    cars = db.session.query(Car).all()

    if not cars:
        return {
            "status": "error",
            "message": "No cars registered",
            "data": [],
        }, HTTP_404_NOT_FOUND
    
    def handleCar(car):
        services = [updateService(service.as_dict()) for service in car.services]
        car = car.as_dict()
        car["services"] = services

        return car 

    resp_data = [handleCar(car) for car in cars]

    return {
        "status": "success",
        "message": f"{len(resp_data)} cars found",
        "data": resp_data,
    }, HTTP_200_OK


@car_bp.get("/<id>")
@validate_response(response_model=CarResponse)
def get_car(id):
    car = db.session.query(Car).filter_by(car_id=id).first()

    if not car:
        return {
            "status": "error",
            "message": "Car does not exist",
            "data": None,
        }, HTTP_404_NOT_FOUND
    
    services = [updateService(service.as_dict()) for service in car.services]
    car = car.as_dict()
    car["services"] = services

    
    resp_data = car

    return {
        "status": "success",
        "message": "Car retrieved successfully",
        "data": resp_data,
    }, HTTP_200_OK


@car_bp.delete("/<id>")
@jwt_required()
def delete_car(id):
    car = db.session.query(Car).filter_by(car_id=id).first()

    if not car:
        return {
            "status": "error",
            "message": "car does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    filename = car.image
    db.session.delete(car)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR
    
    try:
        delete_image(filename=filename)
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR


    return {}, HTTP_204_NO_CONTENT


@car_bp.put("/<id>")
@jwt_required()
@validate_request(request_model=CarCreate)
@validate_response(response_model=CarResponse)
def update_car(id):
    car_query = db.session.query(Car).filter_by(car_id=id)

    if car_query.first() is None:
        return {
            "status": "error",
            "message": "car does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND
    
    data = request.get_json()
    updated_car = car_query.update(data, synchronize_session=False)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR
    
    data['car_id'] = id
    resp_data = data

    return {
        "status": "success",
        "message": "car updated successfully",
        "data": resp_data
    }, HTTP_200_OK
