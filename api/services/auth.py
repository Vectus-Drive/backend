from flask import Blueprint, request, make_response
from ..database import db
from ..models import User, Customer, Employee
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, set_refresh_cookies
from ..utils.helpers import generate_user_id, add_token_to_database, hash_password, verify_password, is_token_revoked, revoke_token
from ..utils.http_status_codes import *
from pydantic import ValidationError
from ..schemas import UserCreate, UserResponse, Role

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth_bp.post("/register")
def register_user():
    try:
        data = request.get_json()
        user_data = UserCreate.model_validate(data)
    except ValidationError as e:
        return {"error": e.errors()[0]}, 400

    username = data["username"]
    role = data["role"]

    # Check if user already exists
    if db.session.query(User).filter_by(username=username).first():
        return {"message": "User already registered"}, HTTP_403_FORBIDDEN

    user_id = generate_user_id()

    # Create the base user
    hashed_pw = hash_password(user_data.password)
    user = User(u_id=user_id, username=username, password=hashed_pw, role=role)

    # Role-specific creation
    common_fields = {
        "customer_id" if role == Role.CUSTOMER else "employee_id": user_id,
        "name": user_data.name,
        "nic": user_data.nic,
        "email": user_data.email,
        "address": user_data.address,
        "image": user_data.image,
        "telephone_no": user_data.telephone_no,
    }

    if role == Role.CUSTOMER:
        db.session.add_all([user, Customer(**common_fields)])
    else:
        db.session.add_all([user, Employee(**common_fields)])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

    response_data = {**data, "user_id": user_id}
    response_data.pop("password")

    return {"success": True, "user": response_data}, HTTP_201_CREATED

@auth_bp.post("/login")
def login_user():
    password = request.json["password"]
    username = request.json["username"]

    if not username or not password:
        return {"error": "Username and password are required"}, HTTP_400_BAD_REQUEST

    user_ = db.session.query(User).filter_by(username=username).first()
    if not user_:
        return {"message": "user is not registered"}, HTTP_403_FORBIDDEN
    
    if verify_password(password, user_.password):

        access_token = create_access_token(identity=str(user_.u_id), additional_claims={"role": user_.role})
        refresh_token = create_refresh_token(identity=str(user_.u_id), additional_claims={"role": user_.role})

        add_token_to_database(refresh_token)

        resp = make_response({'message': 'Login Success'})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, HTTP_200_OK

    return {'message': 'Login Failed'}, HTTP_401_UNAUTHORIZED


@auth_bp.get("/me")
@jwt_required()
def me():
    id = get_jwt_identity()
    role = get_jwt()["role"] 
    response = {
        "id" : id,
        "role" : role
    }
    return response, HTTP_200_OK


@auth_bp.post("/token/refresh")
@jwt_required(refresh=True)
def refresh_user_token():
    jwt_data = get_jwt()
    user_id = get_jwt_identity()
    role = jwt_data.get("role")
    jti = jwt_data.get("jti")

    if is_token_revoked(jti, user_id):
        return {"message": "Refresh token has been revoked"}, HTTP_401_UNAUTHORIZED

    revoke_token(jti, user_id)

    new_access_token = create_access_token(identity=str(user_id), additional_claims={"role": role})
    new_refresh_token = create_refresh_token(identity=str(user_id), additional_claims={"role": role})

    add_token_to_database(new_refresh_token)

    resp = make_response({"message": "Token refresh successful"})
    set_access_cookies(resp, new_access_token)
    set_refresh_cookies(resp, new_refresh_token)

    return resp, HTTP_201_CREATED