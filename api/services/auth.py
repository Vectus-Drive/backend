from flask import Blueprint, request, make_response
from ..database import db
from ..models import User
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, set_refresh_cookies
from ..utils.helpers import add_token_to_database, is_token_revoked, revoke_token
from ..utils.http_status_codes import *

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth_bp.post("/login")
def login_user():
    email = request.json["email"]
    username = request.json["username"]

    if email == "abc@gmail.com" and username == "amila":
        access_token = create_access_token(identity="1")
        refresh_token = create_refresh_token(identity="1")

        add_token_to_database(refresh_token)

        resp = make_response({'message': 'Login Success'})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, HTTP_200_OK

    return {'message': 'Login Failed'}, HTTP_401_UNAUTHORIZED


@auth_bp.get("/me")
@jwt_required()
def me():
    identity = get_jwt_identity()  # reads the token from the cookie
    return {"status" : f'{identity["id"]}'}


@auth_bp.post("/token/refresh")
@jwt_required(refresh=True)
def refresh_user_token():
    id = get_jwt_identity()
    if id:
        new_access_token = create_access_token(id)
        new_refresh_token = create_refresh_token(id)

        resp = make_response({'message': 'Tokens Generation Successful'})
        set_access_cookies(resp, new_access_token)
        set_refresh_cookies(resp, new_refresh_token)
        return resp, HTTP_201_CREATED

    return {'message': 'Token Generation Failed'}, HTTP_401_UNAUTHORIZED
