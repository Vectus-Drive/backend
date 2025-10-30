from flask import Blueprint, request, make_response
from ..database import db
from ..models import Review, Customer
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *
from ..utils.helpers import generate_review_id, validate_request, validate_response
from ..schemas import ReviewCreate, ReviewResponse, ReviewUpdate

review_bp = Blueprint("review", __name__, url_prefix="/api/v1/reviews")


@review_bp.post("/")
@jwt_required()
@validate_request(request_model=ReviewCreate)
@validate_response(response_model=ReviewResponse)
def add_review():
    data = request.get_json()
    customer_id = data["customer_id"]

    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if not customer:
        return {
            "status": "error",
            "message": "Customer does not exist",
            "data": None
        }, HTTP_404_NOT_FOUND

    review_id = generate_review_id()
    data["review_id"] = review_id

    review = Review(**data)
    db.session.add(review)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    resp_data = review.as_dict()

    return {
        "status": "success",
        "message": "Review created successfully",
        "data": resp_data,
    }, HTTP_201_CREATED


@review_bp.get("/")
@validate_response(response_model=ReviewResponse)
def get_reviews():
    customer_id = request.args.get("customer_id")

    if customer_id:
        reviews = db.session.query(Review).filter_by(customer_id=customer_id).all()
    else:
        reviews = db.session.query(Review).all()

    if not reviews:
        return {
            "status": "error",
            "message": "No reviews found",
            "data": [],
    }, HTTP_404_NOT_FOUND

    def handleReview(review):
        customer_name = review.customer.name
        # print(review.customer)
        review = review.as_dict()
        review["customer_name"] = customer_name
        if customer_id:
            del review["customer_id"]
        return review


    resp_data = [handleReview(review) for review in reviews]

    return {
        "status": "success",
        "message": f"{len(resp_data)} reviews found",
        "data": resp_data,
    }, HTTP_200_OK


@review_bp.get("/<id>")
@validate_response(response_model=ReviewResponse)
def get_review(id):
    review = db.session.query(Review).filter_by(review_id=id).first()

    if not review:
        return {
            "status": "error",
            "message": "Review does not exist",
            "data": None,
        }, HTTP_404_NOT_FOUND
    
    customer_name = review.customer.name
    review = review.as_dict()
    review["customer_name"] = customer_name
    resp_data = review

    return {
        "status": "success",
        "message": "Review retrieved successfully",
        "data": resp_data,
    }, HTTP_200_OK


@review_bp.delete("/<id>")
@jwt_required()
def delete_review(id):
    review = db.session.query(Review).filter_by(review_id=id).first()
    if not review:
        return {
            "status": "error",
            "message": "Review not found",
            "data": None,
        }, HTTP_404_NOT_FOUND

    db.session.delete(review)

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


@review_bp.put("/<id>")
@jwt_required()
@validate_request(request_model=ReviewUpdate)
@validate_response(response_model=ReviewResponse)
def update_review(id):
    review_query = db.session.query(Review).filter_by(review_id=id)

    review = review_query.first()

    if not review:
        return {
            "status": "error",
            "message": "Review not found",
            "data": None,
        }, HTTP_404_NOT_FOUND
    
    customer_id = review.customer.customer_id
    data = request.get_json()
    data["customer_id"] = customer_id
    updated_review = review_query.update(data, synchronize_session=False)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    data["review_id"] = id
    resp_data = data

    return {
        "status": "success",
        "message": "Review updated successfully",
        "data": resp_data,
    }, HTTP_200_OK


