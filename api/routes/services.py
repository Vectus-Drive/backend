from flask import Blueprint, request, make_response
from ..database import db
from ..models import Service, Car
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..utils.helpers import generate_service_id, validate_request, validate_response, role_based
from ..schemas import ServiceCreate, ServiceResponse, ServiceUpdate

service_bp = Blueprint("service", __name__, url_prefix="/api/v1/services")


@service_bp.post("/")
@jwt_required()
@role_based()
@validate_request(request_model=ServiceCreate)
@validate_response(response_model=ServiceResponse)
def add_service():
    data = request.get_json()
    car_id = data["car_id"]

    car = Car.query.filter_by(car_id=car_id).first()
    if not car:
        return {
            "status": "error",
            "message": "Car does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    service_id = generate_service_id()
    data["service_id"] = service_id

    service = Service(**data)
    db.session.add(service)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    resp_data = service.as_dict()

    return {
        "status": "success",
        "message": "service created successfully",
        "data": resp_data,
    }, HTTP_201_CREATED


@service_bp.get("/")
@validate_response(response_model=ServiceResponse)
def get_services():
    services = db.session.query(Service).all()

    if not services:
        return {
            "status": "error",
            "message": "No Services found",
            "data": [],
        }, HTTP_404_NOT_FOUND

    resp_data = [service.as_dict() for service in services]

    return {
        "status": "success",
        "message": f"{len(resp_data)} Services found",
        "data": resp_data,
    }, HTTP_200_OK


@service_bp.get("/<id>")
@jwt_required()
@validate_response(response_model=ServiceResponse)
def get_service(id):
    service = db.session.query(Service).filter_by(service_id=id).first()

    if not service:
        return {
            "status": "error",
            "message": "Service not found",
            "data": None,
        }, HTTP_404_NOT_FOUND

    resp_data = service.as_dict()

    return {
        "status": "success",
        "message": "Service retrieved successfully",
        "data": resp_data,
    }, HTTP_200_OK


@service_bp.delete("/<id>")
@jwt_required()
def delete_service(id):
    service = db.session.query(Service).filter_by(service_id=id).first()
    if not service:
        return {
            "status": "error",
            "message": "Service not found",
            "data": None,
        }, HTTP_404_NOT_FOUND

    db.session.delete(service)

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


@service_bp.put("/<id>")
@jwt_required(id)
@validate_request(request_model=ServiceUpdate)
@validate_response(response_model=ServiceResponse)
def update_service(id):
    service_query = db.session.query(Service).filter_by(service_id=id)

    service = service_query.first()

    if not service:
        return {
            "status": "error",
            "message": "Service not found",
            "data": None,
        }, HTTP_404_NOT_FOUND
    
    car_id = service.car.car_id
    data = request.get_json()
    data["car_id"] = car_id
    updated_service = service_query.update(data, synchronize_session=False)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    data["service_id"] = id
    resp_data = data

    return {
        "status": "success",
        "message": "Service updated successfully",
        "data": resp_data,
    }, HTTP_200_OK