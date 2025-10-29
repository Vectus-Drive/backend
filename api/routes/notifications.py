from flask import Blueprint, request, make_response
from ..database import db
from ..models import Notification, User
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..utils.helpers import generate_notification_id, validate_request, validate_response
from ..schemas import NotificationCreate, NotificationResponse, NotificationUpdate

notification_bp = Blueprint("notification", __name__, url_prefix="/api/v1/notifications")


@notification_bp.post("/")
@jwt_required()
@validate_request(request_model=NotificationCreate)
@validate_response(response_model=NotificationResponse)
def add_notification():
    data = request.get_json()
    u_id = data["u_id"]

    user = User.query.filter_by(u_id=u_id).first()
    if not user:
        return {
            "status": "error",
            "message": "User does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    notification_id = generate_notification_id()
    data["notification_id"] = notification_id

    notification = Notification(**data)
    db.session.add(notification)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    resp_data = notification.as_dict()

    return {
        "status": "success",
        "message": "Notification created successfully",
        "data": resp_data,
    }, HTTP_201_CREATED


@notification_bp.get("/")
@validate_response(response_model=NotificationResponse)
def get_notifications():
    user_id = request.args.get("user_id")

    if user_id:
        notifications = db.session.query(Notification).filter_by(u_id=user_id).all()
    else:
        notifications = db.session.query(Notification).all()

    if not notifications:
        return {
            "status": "error",
            "message": "No Notifications found",
            "data": [],
    }, HTTP_404_NOT_FOUND


    resp_data = [notification.as_dict() for notification in notifications]

    return {
        "status": "success",
        "message": f"{len(resp_data)} notifications found",
        "data": resp_data,
    }, HTTP_200_OK


@notification_bp.get("/<id>")
@validate_response(response_model=NotificationResponse)
def get_notification(id):
    notification = db.session.query(Notification).filter_by(notification_id=id).first()

    if not notification:
        return {
            "status": "error",
            "message": "Notification does not exist",
            "data": None,
        }, HTTP_404_NOT_FOUND

    resp_data = notification.as_dict()

    return {
        "status": "success",
        "message": "Notification retrieved successfully",
        "data": resp_data,
    }, HTTP_200_OK


@notification_bp.delete("/<id>")
@jwt_required()
def delete_notification(id):
    notification = db.session.query(Notification).filter_by(notification_id=id).first()
    if not notification:
        return {
            "status": "error",
            "message": "notification not found",
            "data": None,
        }, HTTP_404_NOT_FOUND

    db.session.delete(notification)

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


@notification_bp.put("/<id>")
@jwt_required()
@validate_request(request_model=NotificationUpdate)
@validate_response(response_model=NotificationResponse)
def update_notification(id):
    notification_query = db.session.query(Notification).filter_by(notification_id=id)

    notification = notification_query.first()

    if not notification:
        return {
            "status": "error",
            "message": "Notification not found",
            "data": None,
        }, HTTP_404_NOT_FOUND
    
    u_id = notification.user.u_id
    data = request.get_json()
    data["u_id"] = u_id
    updated_notification = notification_query.update(data, synchronize_session=False)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    data["notification_id"] = id
    resp_data = data

    return {
        "status": "success",
        "message": "Notification updated successfully",
        "data": resp_data,
    }, HTTP_200_OK


