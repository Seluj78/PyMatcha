import os
from functools import wraps

from flask import request
from PyMatcha.errors import BadRequestError
from PyMatcha.errors import UnauthorizedError
from werkzeug.exceptions import BadRequest


def validate_required_params(required):
    def decorator(fn):
        """Decorator that checks for the required parameters"""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            # If the json body is missing something (`,` for example), throw an error
            try:
                data = request.get_json()
            except BadRequest:
                raise BadRequestError("The Json Body is malformed", "Please check it and try again")

            # If the data dict is empty
            if not data:
                raise BadRequestError("Missing json body.", "Please fill your json body")

            missing = []
            for item in required.keys():
                # If a key is missing in the sent data
                if item not in data.keys():
                    missing.append(item)
            if missing:
                raise BadRequestError(
                    "Missing keys {} to create user.".format(missing), "Complete your json body and try again"
                )

            for item in data.keys():
                # If there's an unwanted key in the sent data
                if item not in required.keys():
                    raise BadRequestError(
                        "You can't specify key '{}'.".format(item),
                        "You are only allowed to specify the fields {} "
                        "when creating a user.".format(required.keys()),
                    )

            for key, value in data.items():
                if not value:
                    raise BadRequestError(f"The item {key} cannot be None or empty", "Please try again.")

            wrong_types = [r for r in required.keys() if not isinstance(data[r], required[r])]

            if wrong_types:
                raise BadRequestError(
                    "{} is/are the wrong type.".format(wrong_types), "It/They must be respectively {}".format(required)
                )

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def debug_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("debug-auth-token", None)
        if token:
            if token != os.getenv("DEBUG_AUTH_TOKEN"):
                raise UnauthorizedError("Incorrect debug auth token.", "Try again")
        else:
            raise UnauthorizedError("Missing debug auth token.", "Try again")
        return f(*args, **kwargs)

    return decorated_function
