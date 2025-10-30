import random, string
from datetime import datetime, timezone
from flask_jwt_extended import decode_token
from ..models import Token
from ..database import db
from bcrypt import hashpw, checkpw
from functools import wraps
from flask import jsonify, request
from pydantic import ValidationError
from ..utils.http_status_codes import *

def add_token_to_database(token):
    """
    Save a decoded JWT token into the database.
    """
    decoded_token = decode_token(token)

    jti = decoded_token['jti']
    user_id = decoded_token['sub']
    expires = datetime.fromtimestamp(decoded_token['exp'])

    db_token = Token(
        jti=jti,
        user_id=user_id,
        expires=expires
    )

    db.session.add(db_token)
    db.session.commit()
    db.session.refresh(db_token)


def revoke_token(token_jti, user_id):
    """
    Revoke a token by setting revoked_at to current UTC time.
    """
    token = Token.query.filter_by(jti=token_jti, user_id=user_id).first()

    if not token:
        raise Exception(f"Could not find token {token_jti}")

    token.revoked_at = datetime.now(timezone.utc)
    db.session.commit()


def is_token_revoked(token_jti, user_id):
    """
    Check if a token is revoked.
    Returns True if revoked, False otherwise.
    """
    token = Token.query.filter_by(jti=token_jti, user_id=user_id).first()

    if not token:
        raise Exception(f"Could not find token {token_jti}")

    return token.revoked_at is not None


alphabet = string.ascii_uppercase
numbers = [str(i) for i in range(10)]

def generate_id(size=10):
    id = ""
    for i in range(size):
        rand_num = random.randint(0, 25);
        id += alphabet[rand_num]
        if rand_num % 2 == 0:
            id += random.choice(numbers)
        else:
            rand_num = random.randint(0, 25);
            id += alphabet[rand_num]
    return id

def generate_car_id():
    return "CAR_" + generate_id(10)

def generate_user_id():
    return "USER_" + generate_id(8)

def generate_transaction_id():
    return "TRS_" + generate_id(8)

def generate_booking_id():
    return "BK_" + generate_id(8)

def generate_review_id():
    return "REV_" + generate_id(8)

def generate_service_id():
    return "SERV_" + generate_id(8)

def generate_notification_id():
    return "NT_" + generate_id(8)


import bcrypt

def hash_password(plain_password):
    hashed = hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password, hashed_password):
    return checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

# utils/response_validator.py

def validate_response(model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response, status_code = func(*args, **kwargs)

            try:
                model.parse_obj(response)
            except ValidationError as e:
                # Log validation error and return a 500 error
                return jsonify({
                    "status": "error",
                    "message": "Response validation failed",
                    "details": e.errors()
                }), 500

            return jsonify(response), status_code
        return wrapper
    return decorator

def validate_request(request_model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            if not data:
                return jsonify({
                    "status": "error",
                    "message": "Invalid or missing JSON body"
                }), HTTP_400_BAD_REQUEST

            try:
                request_model.parse_obj(data)
            except ValidationError as e:
                return jsonify({
                    "status": "error",
                    "message": "Request validation failed",
                    "details": e.errors()
                }), HTTP_400_BAD_REQUEST 
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_response(response_model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response_data, status_code = func(*args, **kwargs)
            try:
                response_model.parse_obj(response_data)
            except ValidationError as e:
                return jsonify({
                    "status": "error",
                    "message": "Response validation failed",
                    "data": e.errors()
                }), 500

            return jsonify(response_data), status_code
        return wrapper
    return decorator

def role_based():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            access_token = request.cookies.get('access_token_cookie')
            decoded_token = decode_token(access_token)
            role = decoded_token["role"]
            if role != "employee":
                return jsonify({
                    "status": "error",
                    "message": "Unauthorized to perform this action",
                    "data": None
                }), 401

            return func(*args, **kwargs)
        return wrapper
    return decorator


