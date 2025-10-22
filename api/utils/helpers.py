from datetime import datetime
from flask_jwt_extended import decode_token
from ..models import Token
from ..database import db


def add_token_to_database(token):
    """
    Save a decoded JWT token into the database.
    """
    decoded_token = decode_token(token)

    jti = decoded_token['jti']
    user_id = int(decoded_token['sub'])
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


def is_token_revoked(jwt_payload):
    """
    Check if a token is revoked.
    Returns True if revoked, False otherwise.
    """
    token_jti = jwt_payload['jti']
    user_id = jwt_payload['sub']

    token = Token.query.filter_by(jti=token_jti, user_id=user_id).first()

    if not token:
        raise Exception(f"Could not find token {token_jti}")

    return token.revoked_at is not None
