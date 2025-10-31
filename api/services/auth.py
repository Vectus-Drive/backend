from flask import Blueprint, request, make_response
from ..database import db
from ..models import User, Customer, Employee
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    set_access_cookies,
    set_refresh_cookies,
    unset_refresh_cookies,
    unset_access_cookies
)
from ..utils.helpers import (
    generate_user_id,
    add_token_to_database,
    hash_password,
    verify_password,
    is_token_revoked,
    revoke_token,
    validate_request,
    validate_response,
)
from ..utils.http_status_codes import *
from pydantic import ValidationError
from ..schemas import UserCreate, UserResponse

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.post("/register")
@validate_request(request_model=UserCreate)
@validate_response(response_model=UserResponse)
def register_user():
    data = request.get_json()
    username = data["username"]
    role = data["role"]

    # Check if user already exists
    user_ = db.session.query(User).filter_by(username=username).first()

    if user_:
        return {
            "status": "error",
            "message": "User already registered",
            "data": None,
        }, HTTP_403_FORBIDDEN

    user_id = generate_user_id()

    # Create the base user
    hashed_pw = hash_password(data["password"])
    user = User(u_id=user_id, username=username, password=hashed_pw, role=role)

    image_ = data["image"] if "image" in data else None
    # Role-specific creation
    common_fields = {
        "customer_id" if role == "customer" else "employee_id": user_id,
        "name": data["name"],
        "nic": data["nic"],
        "email": data["email"],
        "address": data["address"],
        "image": image_,
        "telephone_no": data["telephone_no"],
    }

    if role == "customer":
        db.session.add_all([user, Customer(**common_fields)])
    else:
        db.session.add_all([user, Employee(**common_fields)])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "data": str(e),
        }, HTTP_500_INTERNAL_SERVER_ERROR

    resp_data = {"u_id": user_id, "username": data["username"], "role": role}

    return {
        "status": "success",
        "message": "User created successfully",
        "data": resp_data,
    }, HTTP_201_CREATED


@auth_bp.post("/login")
def login_user():
    password = request.json.get("password")
    username = request.json.get("username")

    if not username or not password:
        return {
            "status": "error",
            "message": "Username and password are required",
            "data": None,
        }, HTTP_400_BAD_REQUEST

    user_ = db.session.query(User).filter_by(username=username).first()
    if not user_:
        return {
            "status": "error",
            "message": "User is not registered",
            "data": None,
        }, HTTP_403_FORBIDDEN

    if verify_password(password, user_.password):
        access_token = create_access_token(
            identity=str(user_.u_id), additional_claims={"role": user_.role}
        )
        refresh_token = create_refresh_token(
            identity=str(user_.u_id), additional_claims={"role": user_.role}
        )

        add_token_to_database(refresh_token)

        resp = make_response(
            {"status": "success", "message": "Login successful", "data": None}
        )
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, HTTP_200_OK

    return {
        "status": "error",
        "message": "Login failed",
        "data": None,
    }, HTTP_401_UNAUTHORIZED


@auth_bp.get("/me")
@jwt_required()
def me():
    id = get_jwt_identity()
    role = get_jwt()["role"]
    return {
        "status": "success",
        "message": "User info retrieved successfully",
        "data": {"id": id, "role": role},
    }, HTTP_200_OK


@auth_bp.post("/token/refresh")
@jwt_required(refresh=True)
def refresh_user_token():
    jwt_data = get_jwt()
    user_id = get_jwt_identity()
    role = jwt_data.get("role")
    jti = jwt_data.get("jti")

    if is_token_revoked(jti, user_id):
        return {
            "status": "error",
            "message": "Refresh token has been revoked",
            "data": None,
        }, HTTP_401_UNAUTHORIZED

    revoke_token(jti, user_id)

    new_access_token = create_access_token(
        identity=str(user_id), additional_claims={"role": role}
    )
    new_refresh_token = create_refresh_token(
        identity=str(user_id), additional_claims={"role": role}
    )

    add_token_to_database(new_refresh_token)

    resp = make_response(
        {"status": "success", "message": "Token refresh successful", "data": None}
    )
    set_access_cookies(resp, new_access_token)
    set_refresh_cookies(resp, new_refresh_token)

    return resp, HTTP_201_CREATED


@auth_bp.delete("/delete/<id>")
@jwt_required()
def delete_user(id):
    user = db.session.query(User).filter_by(u_id=id).first()
    if not user:
        return {
            "status": "error",
            "message": "User not found",
            "data": None,
        }, HTTP_404_NOT_FOUND

    db.session.delete(user)

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


@auth_bp.post("/logout")
@jwt_required(refresh=True)
def logout_user():
    jwt_data = get_jwt()
    user_id = get_jwt_identity()
    jti = jwt_data.get("jti")
    
    revoke_token(jti, user_id)

    resp = make_response(
        {"status": "success", "message": "Logout successful", "data": None}
    )
    unset_access_cookies(resp)
    unset_refresh_cookies(resp)
    return resp, HTTP_200_OK
