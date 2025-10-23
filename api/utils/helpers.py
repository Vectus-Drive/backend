import random, string
from datetime import datetime
from flask_jwt_extended import decode_token
from ..models import Token
from ..database import db
from bcrypt import hashpw, checkpw

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

    token.revoked_at = datetime.utcnow()
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


import bcrypt

def hash_password(plain_password):
    hashed = hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password, hashed_password):
    return checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
