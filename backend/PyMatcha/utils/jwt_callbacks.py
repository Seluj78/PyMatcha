import datetime
import logging

from flask import jsonify
from PyMatcha import jwt
from PyMatcha import redis
from PyMatcha.models.user import get_user
from PyMatcha.utils.errors import NotFoundError
from sentry_sdk import configure_scope

logging.debug("Configuring JWT callbacks")


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    resp = {
        "code": 401,
        "error": {
            "message": f"The {expired_token['type']} token has expired",
            "name": "Unauthorized Error",
            "solution": "Try again when you have renewed your token",
            "type": "UnauthorizedError",
        },
        "success": False,
    }
    return jsonify(resp), 401


@jwt.user_loader_callback_loader
def jwt_user_callback(identity):
    try:
        user = get_user(identity["id"])
    except NotFoundError:
        # The user who the server issues the token for was deleted in the db.
        return None

    with configure_scope() as scope:
        scope.user = {"email": user.email, "id": user.id, "username": user.username}
    user.is_online = True
    user.dt_lastseen = datetime.datetime.utcnow()
    user.save()
    return user


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token["jti"]
    entry = redis.get("is_revoked_jti:" + jti)
    if entry is None:
        return True
    return entry == "true"


@jwt.revoked_token_loader
def jwt_revoked_token_callback():
    return (
        jsonify(
            {
                "code": 401,
                "error": {
                    "message": "Token has been revoked.",
                    "name": "Unauthorized Error",
                    "solution": "Please login again",
                    "type": "UnauthorizedError",
                },
                "success": False,
            }
        ),
        401,
    )


@jwt.unauthorized_loader
def no_jwt_callback(error_message):
    return (
        jsonify(
            {
                "code": 401,
                "error": {
                    "message": error_message,
                    "name": "Unauthorized Error",
                    "solution": "Try again",
                    "type": "UnauthorizedError",
                },
                "success": False,
            }
        ),
        401,
    )


@jwt.invalid_token_loader
def jwt_invalid_token_callback(error_message):
    return (
        jsonify(
            {
                "code": 400,
                "error": {
                    "message": error_message,
                    "name": "Bad Request Error",
                    "solution": "Try again (The token is invalid)",
                    "type": "BadRequestError",
                },
                "success": False,
            }
        ),
        400,
    )
