from flask import Blueprint, request, make_response
from ..database import db
from ..models import Review
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *

review_bp = Blueprint("review", __name__, url_prefix="/api/v1/reviews")


@review_bp.post("/")
@jwt_required()
def add_review():
    return {'message': 'add review'}, HTTP_200_OK

@review_bp.get("/")
def get_reviews():
    return {'message': 'get review list'}, HTTP_200_OK

@review_bp.get("/<id>")
def get_review(id):
    return {'message': 'get review by id'}, HTTP_200_OK

@review_bp.delete("/<id>")
@jwt_required()
def delete_review(id):
    return {'message': 'delete review'}, HTTP_200_OK

@review_bp.put("/<id>")
@jwt_required(id)
def update_review():
    return {'message': 'updated review'}, HTTP_200_OK


