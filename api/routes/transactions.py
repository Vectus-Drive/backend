from flask import Blueprint, request, make_response
from ..database import db
from ..models import Transaction
from flask_jwt_extended import jwt_required
from ..utils.http_status_codes import *

transaction_bp = Blueprint("transaction", __name__, url_prefix="/api/v1/transactions")


@transaction_bp.post("/")
@jwt_required()
def add_transaction():
    return {'message': 'add transaction'}, HTTP_200_OK

@transaction_bp.get("/")
def get_transactions():
    return {'message': 'get transaction list'}, HTTP_200_OK

@transaction_bp.get("/<id>")
def get_transaction(id):
    return {'message': 'get transaction by id'}, HTTP_200_OK

@transaction_bp.delete("/<id>")
@jwt_required()
def delete_transaction(id):
    return {'message': 'delete transaction'}, HTTP_200_OK

@transaction_bp.put("/<id>")
@jwt_required()
def update_transaction(id):
    return {'message': 'updated transaction'}, HTTP_200_OK


